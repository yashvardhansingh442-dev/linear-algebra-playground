import math

from determinant import determinant


def _validate_square(M):
    """Validate that M is a non-empty, rectangular, square matrix. Returns size n."""
    if not M:
        raise ValueError("Matrix cannot be empty.")
    if any(len(row) != len(M[0]) for row in M):
        raise ValueError("Matrix is not rectangular.")
    rows = len(M)
    cols = len(M[0])
    if rows != cols:
        raise ValueError(f"Eigen computations require a square matrix, got {rows}x{cols}.")
    return rows


def _trace(M):
    """Sum of the diagonal entries."""
    return sum(M[i][i] for i in range(len(M)))


# ---------------------------------------------------------------------------
# Characteristic polynomial (small matrices only: n = 2 or 3)
# ---------------------------------------------------------------------------

def characteristic_polynomial(A):
    """
    Return the coefficients [c_n, c_{n-1}, ..., c_0] of the characteristic
    polynomial det(A - lambda*I), highest power first, so they can be fed
    straight into a polynomial root-finder.

    Derived by hand from known identities (not by symbolically expanding
    the determinant), which is only practical for n = 2 or 3:
        n = 2: lambda^2 - trace(A)*lambda + det(A)
        n = 3: -lambda^3 + trace(A)*lambda^2 - (sum of principal 2x2 minors)*lambda + det(A)
               (negated below so the leading coefficient is +1, matching the n=2 case)
    """
    n = _validate_square(A)

    if n == 2:
        tr = _trace(A)
        det = determinant(A)
        return [1, -tr, det]

    if n == 3:
        tr = _trace(A)
        det = determinant(A)
        # Sum of the three principal 2x2 minors (delete row i and column i)
        minors_sum = 0
        for i in range(3):
            rows = [r for r in range(3) if r != i]
            sub = [[A[r][c] for c in range(3) if c != i] for r in rows]
            minors_sum += determinant(sub)
        return [1, -tr, minors_sum, -det]

    raise NotImplementedError(
        "characteristic_polynomial is only implemented for 2x2 and 3x3 matrices. "
        "Use power_iteration for larger matrices."
    )


def _solve_quadratic(coeffs):
    """Solve a*x^2 + b*x + c = 0. Returns a list of real roots (may repeat)."""
    a, b, c = coeffs
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        raise ValueError("Matrix has complex eigenvalues; this repo only handles the real case.")
    sqrt_disc = math.sqrt(discriminant)
    return [(-b + sqrt_disc) / (2 * a), (-b - sqrt_disc) / (2 * a)]


def eigenvalues(A):
    """
    Compute the eigenvalues of a 2x2 or 3x3 matrix from its characteristic
    polynomial. Real roots only.
    """
    coeffs = characteristic_polynomial(A)

    if len(coeffs) == 3:
        return _solve_quadratic(coeffs)

    # Cubic case: use NumPy purely as a general polynomial root-finder,
    # not as a linear-algebra eigenvalue solver -- the polynomial itself
    # was derived by hand above.
    import numpy as np
    roots = np.roots(coeffs)
    if any(abs(r.imag) > 1e-9 for r in roots):
        raise ValueError("Matrix has complex eigenvalues; this repo only handles the real case.")
    return sorted(float(r.real) for r in roots)


# ---------------------------------------------------------------------------
# Eigenvectors: solve (A - lambda*I)v = 0 by hand via Gaussian elimination
# ---------------------------------------------------------------------------

def _null_space_vector(M, tol=1e-9):
    """
    Find one non-trivial vector v with M @ v = 0, assuming M is (numerically)
    singular, via row reduction with a free-variable back-substitution.
    """
    n = len(M)
    aug = [row[:] for row in M]
    pivot_cols = []
    row = 0

    for col in range(n):
        pivot_row = None
        best = tol
        for r in range(row, n):
            if abs(aug[r][col]) > best:
                best = abs(aug[r][col])
                pivot_row = r
        if pivot_row is None:
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
        if row == n:
            break

    free_cols = [c for c in range(n) if c not in pivot_cols]
    if not free_cols:
        raise ValueError("No free variable found; matrix was not singular at this eigenvalue.")

    free_col = free_cols[0]
    v = [0.0] * n
    v[free_col] = 1.0
    for i, pc in enumerate(pivot_cols):
        v[pc] = -aug[i][free_col]
    return v


def _normalize(v):
    """Scale v to unit length."""
    norm = math.sqrt(sum(x * x for x in v))
    return [x / norm for x in v]


def eigenvector_for(A, lam):
    """Find a unit eigenvector of A for eigenvalue lam by solving (A - lam*I)v = 0."""
    n = len(A)
    shifted = [[A[i][j] - (lam if i == j else 0) for j in range(n)] for i in range(n)]
    v = _null_space_vector(shifted)
    return _normalize(v)


def eigen(A):
    """Return (eigenvalues, eigenvectors) for a 2x2 or 3x3 matrix."""
    vals = eigenvalues(A)
    vecs = [eigenvector_for(A, lam) for lam in vals]
    return vals, vecs


# ---------------------------------------------------------------------------
# Power iteration: dominant eigenvalue/eigenvector for larger matrices
# ---------------------------------------------------------------------------

def power_iteration(A, num_iterations=1000, tol=1e-10):
    """
    Estimate the dominant eigenvalue and eigenvector of A using power iteration:
    repeatedly apply A to a vector and renormalize; it converges toward the
    eigenvector for the largest-magnitude eigenvalue. The eigenvalue is then
    read off with the Rayleigh quotient (v^T A v) / (v^T v).
    """
    n = _validate_square(A)
    v = [1.0] * n  # arbitrary non-zero starting vector
    v = _normalize(v)

    prev_estimate = None
    for _ in range(num_iterations):
        Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        v = _normalize(Av)

        Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        estimate = sum(v[i] * Av[i] for i in range(n))  # Rayleigh quotient (v is unit length)

        if prev_estimate is not None and abs(estimate - prev_estimate) < tol:
            break
        prev_estimate = estimate

    return estimate, v


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    A = [
        [4, 1],
        [2, 3]
    ]
    B = [
        [2, -1, 0],
        [-1, 2, -1],
        [0, -1, 2]
    ]

    for name, M in [("A (2x2)", A), ("B (3x3)", B)]:
        print(f"Matrix {name}:")
        for row in M:
            print(row)

        vals, vecs = eigen(M)
        print("Eigenvalues:", [round(v, 4) for v in vals])
        for lam, vec in zip(vals, vecs):
            print(f"  eigenvector for {round(lam, 4)}:", [round(x, 4) for x in vec])

        try:
            import numpy as np
            np_vals, np_vecs = np.linalg.eig(M)
            print("NumPy eigenvalues:", sorted(round(float(v), 4) for v in np_vals))

            # Verify our (value, vector) pairs actually satisfy A v = lambda v
            all_valid = True
            for lam, vec in zip(vals, vecs):
                Av = [sum(M[i][j] * vec[j] for j in range(len(M))) for i in range(len(M))]
                lv = [lam * x for x in vec]
                if not all(abs(Av[i] - lv[i]) < 1e-6 for i in range(len(M))):
                    all_valid = False
            print("A v == lambda v for all pairs:", all_valid)
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

    print("Power iteration on B (dominant eigenvalue/eigenvector):")
    dom_val, dom_vec = power_iteration(B)
    print("Dominant eigenvalue:", round(dom_val, 4))
    print("Dominant eigenvector:", [round(x, 4) for x in dom_vec])

    try:
        import numpy as np
        np_vals, _ = np.linalg.eig(B)
        print("NumPy largest |eigenvalue|:", round(float(max(np_vals, key=abs)), 4))
    except ImportError:
        pass

    # Complex-eigenvalue case should raise a clear error
    try:
        eigenvalues([[0, -1], [1, 0]])  # rotation matrix: eigenvalues are +-i
        print("ERROR: should have raised")
    except ValueError as e:
        print("\nRaised correctly:", e)
