import math
import warnings
import random

from .determinant import determinant
from .utils import as_square_matrix, mat_vec, norm, max_abs, print_matrix

# Relative tolerance used to decide when roots of a polynomial coincide.
_ROOT_TOL = 1e-12


def _trace(M):
    """Sum of the diagonal entries."""
    return sum(M[i][i] for i in range(len(M)))


# ---------------------------------------------------------------------------
# Characteristic polynomial (small matrices only: n = 2 or 3)
# ---------------------------------------------------------------------------

def characteristic_polynomial(A):
    """
    Return the coefficients [c_n, c_{n-1}, ..., c_0] of the characteristic
    polynomial det(lambda*I - A), highest power first, normalised so the
    leading coefficient is +1.

    Derived by hand from known identities (not by symbolically expanding
    the determinant), which is only practical for n = 2 or 3:
        n = 2: lambda^2 - trace(A)*lambda + det(A)
        n = 3: lambda^3 - trace(A)*lambda^2 + (sum of principal 2x2 minors)*lambda - det(A)
    """
    A = as_square_matrix(A, "Eigen computations")
    n = len(A)

    if n == 2:
        return [1, -_trace(A), determinant(A)]

    if n == 3:
        # Sum of the three principal 2x2 minors (delete row i and column i)
        minors_sum = 0
        for i in range(3):
            sub = [[A[r][c] for c in range(3) if c != i] for r in range(3) if r != i]
            minors_sum += determinant(sub)
        return [1, -_trace(A), minors_sum, -determinant(A)]

    raise NotImplementedError(
        "characteristic_polynomial is only implemented for 2x2 and 3x3 matrices. "
        "Use power_iteration for larger matrices."
    )


_COMPLEX_MSG = "Matrix has complex eigenvalues; this repo only handles the real case."


def _solve_quadratic(coeffs):
    """Solve x^2 + b*x + c = 0 (a = 1). Returns real roots, ascending."""
    _, b, c = coeffs
    discriminant = b * b - 4 * c
    if discriminant < 0:
        # Rounding can push a true double root slightly negative.
        if discriminant < -_ROOT_TOL * max(b * b, abs(4 * c)):
            raise ValueError(_COMPLEX_MSG)
        discriminant = 0.0
    root = math.sqrt(discriminant)
    return sorted([(-b + root) / 2, (-b - root) / 2])


def _solve_cubic(coeffs):
    """
    Real roots of x^3 + b*x^2 + c*x + d = 0, ascending, with multiplicity.

    Hand-rolled (no numpy.roots): shift to the depressed cubic
        t^3 + p*t + q = 0,   x = t - b/3
    and use the discriminant  D = -(4p^3 + 27q^2)  to pick the case:
        D > 0  -> three distinct real roots (trigonometric form)
        D ~ 0  -> a repeated root (closed form, exact to rounding)
        D < 0  -> one real + two complex roots -> unsupported, raise
    Detecting D ~ 0 with a tolerance matters: a matrix like the identity
    has a triple root, and rounding noise would otherwise make it look
    complex.
    """
    _, b, c, d = coeffs
    shift = b / 3
    p = c - b * b / 3
    q = 2 * b ** 3 / 27 - b * c / 3 + d

    coef_scale = max(abs(b), math.sqrt(abs(c)), abs(d) ** (1 / 3))
    if abs(p) <= _ROOT_TOL * coef_scale ** 2 and abs(q) <= _ROOT_TOL * coef_scale ** 3:
        return [-shift] * 3  # triple root

    disc = -(4 * p ** 3 + 27 * q * q)
    scale = max(abs(4 * p ** 3), 27 * q * q)

    if disc < -_ROOT_TOL * scale:
        raise ValueError(_COMPLEX_MSG)

    if disc <= _ROOT_TOL * scale:
        # One simple root and one double root.
        simple = 3 * q / p
        double = -3 * q / (2 * p)
        return sorted([simple - shift, double - shift, double - shift])

    m = 2 * math.sqrt(-p / 3)
    arg = (3 * q) / (p * m)
    theta = math.acos(max(-1.0, min(1.0, arg))) / 3
    return sorted(m * math.cos(theta - 2 * math.pi * k / 3) - shift for k in range(3))


def eigenvalues(A):
    """
    Compute the eigenvalues of a 2x2 or 3x3 matrix from its characteristic
    polynomial, ascending, repeated according to algebraic multiplicity.
    Real roots only.
    """
    coeffs = characteristic_polynomial(A)
    if len(coeffs) == 3:
        return _solve_quadratic(coeffs)
    return _solve_cubic(coeffs)


# ---------------------------------------------------------------------------
# Eigenvectors: solve (A - lambda*I)v = 0 by hand via Gauss-Jordan elimination
# ---------------------------------------------------------------------------

def _null_space_basis(M, tol=None):
    """
    Basis for the null space of a square matrix M, via reduced row echelon
    form: one basis vector per free column (free variable set to 1, the
    pivot variables read off from the reduced rows).

    A pivot counts as zero below `tol` (default 1e-9 * max(1, max|m_ij|)).
    """
    n = len(M)
    aug = [[float(x) for x in row] for row in M]
    if tol is None:
        tol = 1e-9 * max(1.0, max_abs(aug))

    pivot_cols = []
    row = 0
    for col in range(n):
        if row == n:
            break
        pivot_row = max(range(row, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) <= tol:
            continue  # no usable pivot in this column -> it's a free column

        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_val = aug[row][col]
        aug[row] = [x / pivot_val for x in aug[row]]

        for r in range(n):
            if r != row:
                factor = aug[r][col]
                aug[r] = [aug[r][k] - factor * aug[row][k] for k in range(n)]

        pivot_cols.append(col)
        row += 1

    basis = []
    for free_col in (c for c in range(n) if c not in pivot_cols):
        v = [0.0] * n
        v[free_col] = 1.0
        for i, pc in enumerate(pivot_cols):
            v[pc] = -aug[i][free_col]
        basis.append(v)
    return basis


def _normalize(v):
    """Scale v to unit length."""
    length = norm(v)
    if length == 0:
        raise ValueError("Cannot normalize the zero vector.")
    return [x / length for x in v]


def eigenspace(A, lam):
    """
    Unit-length basis vectors for the eigenspace of A at eigenvalue `lam`,
    found by solving (A - lam*I)v = 0. The basis has one vector per free
    variable, so a repeated eigenvalue can yield several independent vectors
    (e.g. the identity matrix has a full basis for lam = 1). The vectors are
    independent but not orthogonalised.
    """
    A = as_square_matrix(A, "Eigen computations")
    n = len(A)
    shifted = [[A[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
    basis = _null_space_basis(shifted)
    if not basis:
        # `lam` carries rounding error; retry with a looser pivot tolerance.
        basis = _null_space_basis(shifted, tol=1e-6 * max(1.0, max_abs(shifted)))
    if not basis:
        raise ValueError(f"{lam} is not an eigenvalue of A (A - lam*I is invertible).")
    return [_normalize(v) for v in basis]


def eigenvector_for(A, lam):
    """Find one unit eigenvector of A for eigenvalue lam by solving (A - lam*I)v = 0."""
    return eigenspace(A, lam)[0]


def eigen(A):
    """
    Return (values, vectors) for a 2x2 or 3x3 matrix; vectors[i] is a unit
    eigenvector for values[i].

    A repeated eigenvalue appears once per independent eigenvector it has.
    If len(values) < n, the matrix is *defective*: some eigenvalue has fewer
    independent eigenvectors than its multiplicity, so A cannot be
    diagonalised (e.g. [[2, 1], [0, 2]]).
    """
    vals = eigenvalues(A)

    # Group (numerically) equal eigenvalues, remembering their multiplicity.
    groups = []
    for lam in vals:
        if groups and abs(lam - groups[-1][0]) <= 1e-7 * max(1.0, abs(lam)):
            groups[-1][1] += 1
        else:
            groups.append([lam, 1])

    out_vals, out_vecs = [], []
    for lam, multiplicity in groups:
        for v in eigenspace(A, lam)[:multiplicity]:
            out_vals.append(lam)
            out_vecs.append(v)
    return out_vals, out_vecs


# ---------------------------------------------------------------------------
# Power iteration: dominant eigenvalue/eigenvector for larger matrices
# ---------------------------------------------------------------------------

def power_iteration(A, num_iterations=1000, tol=1e-10, start=None):
    """
    Estimate the dominant eigenvalue and eigenvector of A using power iteration:
    repeatedly apply A to a vector and renormalize; it converges toward the
    eigenvector for the largest-magnitude eigenvalue. The eigenvalue is read
    off with the Rayleigh quotient (v^T A v) / (v^T v).

    Stops when the residual ||Av - lambda*v|| <= tol * max(1, |lambda|).
    If that doesn't happen within `num_iterations`, a RuntimeWarning is
    issued and the best estimate so far is returned -- this happens when the
    two largest |eigenvalues| are (nearly) equal, e.g. +1 and -1.

    `start` is the initial vector; by default a fixed pseudo-random one, so
    results are reproducible but it is (almost surely) not orthogonal to the
    dominant eigenvector, which would stall the method.
    """
    A = as_square_matrix(A, "Power iteration")
    n = len(A)
    if num_iterations < 1:
        raise ValueError("num_iterations must be at least 1.")

    if start is None:
        rng = random.Random(0)
        start = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    elif len(start) != n:
        raise ValueError(f"start has {len(start)} entries but A is {n}x{n}.")
    v = _normalize([float(x) for x in start])

    lam = 0.0
    for _ in range(num_iterations):
        Av = mat_vec(A, v)
        Av_norm = norm(Av)
        if Av_norm == 0:
            return 0.0, v  # v is in the null space: eigenvalue 0

        lam = sum(vi * wi for vi, wi in zip(v, Av))  # Rayleigh quotient (v is unit length)
        residual = norm([wi - lam * vi for vi, wi in zip(v, Av)])
        if residual <= tol * max(1.0, abs(lam)):
            return lam, v
        v = [x / Av_norm for x in Av]

    warnings.warn(
        f"power_iteration did not converge in {num_iterations} iterations "
        f"(residual {residual:.2e}); the two largest |eigenvalues| may be equal.",
        RuntimeWarning,
        stacklevel=2,
    )
    return lam, v


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    def check(M):
        print_matrix(M, "Matrix")
        vals, vecs = eigen(M)
        print("Eigenvalues:", [round(v, 4) for v in vals])
        for lam, vec in zip(vals, vecs):
            print(f"  eigenvector for {round(lam, 4)}:", [round(x, 4) + 0.0 for x in vec])
        if len(vals) < len(M):
            print("  -> defective: fewer independent eigenvectors than n")

        # Verify our (value, vector) pairs actually satisfy A v = lambda v
        ok = all(
            all(abs(a - lam * x) < 1e-6 for a, x in zip(mat_vec(M, vec), vec))
            for lam, vec in zip(vals, vecs)
        )
        print("A v == lambda v for all pairs:", ok)
        try:
            import numpy as np
            print("NumPy eigenvalues:", sorted(round(float(v), 4) for v in np.linalg.eigvals(M)))
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

    check([[4, 1], [2, 3]])                                # 2x2, distinct
    check([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])           # 3x3, distinct
    check([[2, 0, 0], [0, 2, 0], [0, 0, 3]])               # repeated, full eigenspace
    check([[2, 1], [0, 2]])                                # repeated, defective

    B = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
    print("Power iteration on B (dominant eigenvalue/eigenvector):")
    dom_val, dom_vec = power_iteration(B)
    print("Dominant eigenvalue:", round(dom_val, 4))
    print("Dominant eigenvector:", [round(x, 4) + 0.0 for x in dom_vec])
    try:
        import numpy as np
        print("NumPy largest |eigenvalue|:", round(float(max(np.linalg.eigvals(B), key=abs)), 4))
    except ImportError:
        pass

    # Complex-eigenvalue case should raise a clear error
    try:
        eigenvalues([[0, -1], [1, 0]])  # rotation matrix: eigenvalues are +-i
        print("ERROR: should have raised")
    except ValueError as e:
        print("\nRaised correctly:", e)
