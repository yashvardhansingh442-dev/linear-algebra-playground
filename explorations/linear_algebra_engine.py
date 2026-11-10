"""
ADVANCED LINEAR ALGEBRA ENGINE
==============================

Algorithms:
- LU decomposition with partial pivoting
- Householder QR decomposition
- Jacobi symmetric eigensolver
- Shifted QR eigenvalue algorithm
- One-sided Jacobi SVD
- Moore-Penrose pseudoinverse
- Least-squares solver
- Conjugate gradient
- Power and inverse power iteration
- Gram-Schmidt orthogonalization
- Matrix norms and condition numbers
- Cholesky decomposition

Core algorithms are implemented manually.
NumPy is used for numerical array storage and elementary operations.
"""

from dataclasses import dataclass
import numpy as np


EPS = 1e-12


def matrix(A):
    A = np.asarray(A, dtype=float)

    if A.ndim != 2:
        raise ValueError("Expected a two-dimensional matrix")

    if not np.all(np.isfinite(A)):
        raise ValueError("Matrix contains non-finite values")

    return A.copy()


def vector(b):
    b = np.asarray(b, dtype=float)

    if b.ndim != 1:
        raise ValueError("Expected a one-dimensional vector")

    return b.copy()


def require_square(A):
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square")


@dataclass
class LUResult:
    P: np.ndarray
    L: np.ndarray
    U: np.ndarray

    def solve(self, b):
        b = vector(b)

        n = self.U.shape[0]

        if len(b) != n:
            raise ValueError("Dimension mismatch")

        y = np.zeros(n)

        for i in range(n):
            y[i] = self.P[i] @ b - self.L[i, :i] @ y[:i]

        x = np.zeros(n)

        for i in range(n - 1, -1, -1):
            if abs(self.U[i, i]) < EPS:
                raise np.linalg.LinAlgError("Singular matrix")

            x[i] = (
                y[i] - self.U[i, i + 1:] @ x[i + 1:]
            ) / self.U[i, i]

        return x


# ---------------------------------------------------------
# 1. LU DECOMPOSITION WITH PARTIAL PIVOTING
# ---------------------------------------------------------

def lu_decomposition(A):
    A = matrix(A)
    require_square(A)

    n = len(A)
    U = A.copy()
    L = np.eye(n)
    P = np.eye(n)

    for k in range(n):

        pivot = k + np.argmax(np.abs(U[k:, k]))

        if abs(U[pivot, k]) < EPS:
            raise np.linalg.LinAlgError("Singular matrix")

        if pivot != k:
            U[[k, pivot]] = U[[pivot, k]]
            P[[k, pivot]] = P[[pivot, k]]

            if k:
                L[[k, pivot], :k] = L[[pivot, k], :k]

        for i in range(k + 1, n):
            factor = U[i, k] / U[k, k]

            L[i, k] = factor
            U[i, k:] -= factor * U[k, k:]

            U[i, k] = 0.0

    return LUResult(P, L, U)


# ---------------------------------------------------------
# 2. HOUSEHOLDER QR DECOMPOSITION
# ---------------------------------------------------------

def householder_qr(A):
    A = matrix(A)

    m, n = A.shape
    R = A.copy()
    Q = np.eye(m)

    for k in range(min(m, n)):

        x = R[k:, k].copy()
        norm = np.linalg.norm(x)

        if norm < EPS:
            continue

        alpha = -np.copysign(norm, x[0])
        x[0] -= alpha

        vnorm = np.linalg.norm(x)

        if vnorm < EPS:
            continue

        v = x / vnorm

        R[k:, k:] -= 2 * np.outer(
            v, v @ R[k:, k:]
        )

        Q[:, k:] -= 2 * np.outer(
            Q[:, k:] @ v, v
        )

    return Q, R


# ---------------------------------------------------------
# 3. JACOBI SYMMETRIC EIGENVALUE ALGORITHM
# ---------------------------------------------------------

def jacobi_eigen(A, tolerance=EPS, max_iterations=10000):
    A = matrix(A)
    require_square(A)

    if not np.allclose(A, A.T, atol=tolerance):
        raise ValueError("Matrix must be symmetric")

    n = len(A)
    V = np.eye(n)

    for _ in range(max_iterations):

        p, q = np.unravel_index(
            np.argmax(np.abs(np.triu(A, 1))),
            (n, n)
        )

        if abs(A[p, q]) < tolerance:
            break

        tau = (A[q, q] - A[p, p]) / (2 * A[p, q])

        t = np.copysign(1.0, tau) / (
            abs(tau) + np.sqrt(1 + tau * tau)
        )

        c = 1 / np.sqrt(1 + t * t)
        s = t * c

        app = A[p, p]
        aqq = A[q, q]
        apq = A[p, q]

        A[p, p] = app - t * apq
        A[q, q] = aqq + t * apq
        A[p, q] = A[q, p] = 0.0

        for k in range(n):

            if k != p and k != q:
                akp = A[k, p]
                akq = A[k, q]

                A[k, p] = A[p, k] = c * akp - s * akq
                A[k, q] = A[q, k] = s * akp + c * akq

            vkp = V[k, p]
            vkq = V[k, q]

            V[k, p] = c * vkp - s * vkq
            V[k, q] = s * vkp + c * vkq

    values = np.diag(A).copy()
    order = np.argsort(values)[::-1]

    return values[order], V[:, order]


# ---------------------------------------------------------
# 4. SHIFTED QR EIGENVALUE ALGORITHM
# For real symmetric matrices
# ---------------------------------------------------------

def symmetric_qr_eigen(A, tolerance=EPS, max_iterations=5000):
    A = matrix(A)
    require_square(A)

    if not np.allclose(A, A.T, atol=tolerance):
        raise ValueError("Matrix must be symmetric")

    n = len(A)
    V = np.eye(n)

    for _ in range(max_iterations):

        off_diagonal = np.sqrt(
            np.sum(np.triu(A, 1) ** 2)
        )

        if off_diagonal < tolerance:
            break

        # Wilkinson-style shift for the trailing 2x2 block
        if n > 1:
            a = A[-2, -2]
            b = A[-2, -1]
            d = A[-1, -1]

            delta = (a - d) / 2

            shift = d - (
                np.copysign(1.0, delta) * b * b
                / (abs(delta) + np.sqrt(delta**2 + b*b))
            )
        else:
            shift = A[0, 0]

        Q, R = householder_qr(A - shift * np.eye(n))

        A = R @ Q + shift * np.eye(n)
        A = (A + A.T) / 2

        V = V @ Q

    values = np.diag(A)
    order = np.argsort(values)[::-1]

    return values[order], V[:, order]


# ---------------------------------------------------------
# 5. ONE-SIDED JACOBI SVD
# ---------------------------------------------------------

def jacobi_svd(A, tolerance=EPS, max_sweeps=1000):
    A = matrix(A)

    m, n = A.shape
    B = A.copy()
    V = np.eye(n)

    for _ in range(max_sweeps):

        changed = False

        for p in range(n):
            for q in range(p + 1, n):

                alpha = B[:, p] @ B[:, p]
                beta = B[:, q] @ B[:, q]
                gamma = B[:, p] @ B[:, q]

                if alpha == 0 or beta == 0:
                    continue

                if abs(gamma) <= tolerance * np.sqrt(alpha * beta):
                    continue

                zeta = (beta - alpha) / (2 * gamma)

                t = np.copysign(1.0, zeta) / (
                    abs(zeta) + np.sqrt(1 + zeta*zeta)
                )

                c = 1 / np.sqrt(1 + t*t)
                s = c * t

                bp = B[:, p].copy()
                bq = B[:, q].copy()

                B[:, p] = c * bp - s * bq
                B[:, q] = s * bp + c * bq

                vp = V[:, p].copy()
                vq = V[:, q].copy()

                V[:, p] = c * vp - s * vq
                V[:, q] = s * vp + c * vq

                changed = True

        if not changed:
            break

    singular_values = np.linalg.norm(B, axis=0)
    order = np.argsort(singular_values)[::-1]

    singular_values = singular_values[order]
    V = V[:, order]
    B = B[:, order]

    U = np.zeros((m, n))

    for j, sigma in enumerate(singular_values):
        if sigma > tolerance:
            U[:, j] = B[:, j] / sigma

    return U, singular_values, V.T


# ---------------------------------------------------------
# 6. MOORE-PENROSE PSEUDOINVERSE
# ---------------------------------------------------------

def pseudoinverse(A, tolerance=EPS):
    U, S, VT = jacobi_svd(A, tolerance)

    reciprocal = np.zeros_like(S)
    reciprocal[S > tolerance * max(S, default=0)] = (
        1 / S[S > tolerance * max(S, default=0)]
    )

    return VT.T @ np.diag(reciprocal) @ U.T


# ---------------------------------------------------------
# 7. LEAST SQUARES
# ---------------------------------------------------------

def least_squares(A, b):
    A = matrix(A)
    b = vector(b)

    if A.shape[0] != len(b):
        raise ValueError("Dimension mismatch")

    return pseudoinverse(A) @ b


# ---------------------------------------------------------
# 8. CONJUGATE GRADIENT
# ---------------------------------------------------------

def conjugate_gradient(
    A, b, x0=None, tolerance=1e-10, max_iterations=10000
):
    A = matrix(A)
    b = vector(b)

    require_square(A)

    if A.shape[0] != len(b):
        raise ValueError("Dimension mismatch")

    if not np.allclose(A, A.T, atol=tolerance):
        raise ValueError("Matrix must be symmetric")

    if np.min(np.linalg.eigvalsh(A)) <= 0:
        raise ValueError("Matrix must be positive definite")

    x = np.zeros_like(b) if x0 is None else vector(x0)

    r = b - A @ x
    p = r.copy()
    rs = r @ r

    for iteration in range(max_iterations):

        if np.sqrt(rs) < tolerance:
            return x, iteration

        Ap = A @ p
        denominator = p @ Ap

        if denominator <= 0:
            raise ValueError("Positive definiteness violated")

        alpha = rs / denominator

        x += alpha * p
        r -= alpha * Ap

        rs_new = r @ r

        beta = rs_new / rs
        p = r + beta * p

        rs = rs_new

    raise RuntimeError("Conjugate gradient did not converge")


# ---------------------------------------------------------
# 9. POWER ITERATION
# ---------------------------------------------------------

def power_iteration(A, tolerance=1e-10, max_iterations=10000):
    A = matrix(A)
    require_square(A)

    n = len(A)
    x = np.ones(n)
    x /= np.linalg.norm(x)

    for _ in range(max_iterations):

        y = A @ x
        norm = np.linalg.norm(y)

        if norm < EPS:
            return 0.0, x

        x_new = y / norm

        if min(
            np.linalg.norm(x_new - x),
            np.linalg.norm(x_new + x)
        ) < tolerance:
            x = x_new
            break

        x = x_new

    eigenvalue = x @ A @ x

    return eigenvalue, x


# ---------------------------------------------------------
# 10. INVERSE POWER ITERATION
# Eigenvalue nearest zero. Uses LU solves, never forms A^-1.
# shortcut: fixed all-ones start vector; if it is orthogonal to the
# target eigenvector the result is wrong, so pass a random x0 then.
# ---------------------------------------------------------

def inverse_power_iteration(
    A, x0=None, tolerance=1e-10, max_iterations=10000
):
    A = matrix(A)
    require_square(A)

    factorization = lu_decomposition(A)
    n = len(A)

    x = np.ones(n) if x0 is None else vector(x0)
    x /= np.linalg.norm(x)

    for _ in range(max_iterations):
        y = factorization.solve(x)
        norm = np.linalg.norm(y)

        if norm < EPS:
            raise np.linalg.LinAlgError("Singular matrix")

        x_new = y / norm

        done = min(
            np.linalg.norm(x_new - x),
            np.linalg.norm(x_new + x)
        ) < tolerance

        x = x_new

        if done:
            return x @ A @ x, x

    raise RuntimeError("Inverse power iteration did not converge")


# ---------------------------------------------------------
# 11. GRAM-SCHMIDT ORTHOGONALIZATION
# ---------------------------------------------------------

def gram_schmidt(A, tolerance=EPS):
    A = matrix(A)

    Q = []

    for j in range(A.shape[1]):

        v = A[:, j].copy()

        for q in Q:
            v -= (q @ v) * q

        norm = np.linalg.norm(v)

        if norm > tolerance:
            Q.append(v / norm)

    return np.column_stack(Q) if Q else np.empty((A.shape[0], 0))


# ---------------------------------------------------------
# 12. MATRIX CONDITION NUMBER
# ---------------------------------------------------------

def condition_number(A, p=2):
    A = matrix(A)

    if p == 2:
        singular_values = jacobi_svd(A)[1]

        if len(singular_values) == 0 or singular_values[-1] < EPS:
            return float("inf")

        return singular_values[0] / singular_values[-1]

    raise NotImplementedError("Only spectral condition number supported")


# ---------------------------------------------------------
# 13. CHOLESKY DECOMPOSITION: A = L @ L.T
# ---------------------------------------------------------

def cholesky_decomposition(A, tolerance=EPS):
    A = matrix(A)
    require_square(A)

    if not np.allclose(A, A.T, atol=tolerance):
        raise ValueError("Matrix must be symmetric")

    n = len(A)
    L = np.zeros_like(A)

    for i in range(n):
        for j in range(i + 1):

            value = A[i, j] - L[i, :j] @ L[j, :j]

            if i == j:
                if value <= tolerance:
                    raise ValueError(
                        "Matrix must be positive definite"
                    )
                L[i, j] = np.sqrt(value)
            else:
                L[i, j] = value / L[j, j]

    return L


# ---------------------------------------------------------
# 14. DEMONSTRATION + SELF-CHECKS
# ---------------------------------------------------------

if __name__ == "__main__":

    A = np.array([
        [4., 1., 2.],
        [1., 5., 1.],
        [2., 1., 6.]
    ])

    b = np.array([7., 7., 9.])

    print("\nLU DECOMPOSITION")
    lu = lu_decomposition(A)

    print("L:\n", lu.L)
    print("U:\n", lu.U)
    print("P:\n", lu.P)
    print("Solution:", lu.solve(b))
    assert np.allclose(A @ lu.solve(b), b)

    print("\nHOUSEHOLDER QR")
    Q, R = householder_qr(A)

    print("Q:\n", Q)
    print("R:\n", R)
    print("Reconstruction error:", np.linalg.norm(A - Q @ R))
    assert np.allclose(Q @ R, A)

    print("\nJACOBI EIGENVALUES")
    values, vectors = jacobi_eigen(A)

    print(values)
    print("Eigenvectors:\n", vectors)
    assert np.allclose(values, np.linalg.eigvalsh(A)[::-1])

    print("\nSHIFTED QR EIGENVALUES")
    qr_values = symmetric_qr_eigen(A)[0]
    print(qr_values)
    assert np.allclose(qr_values, np.linalg.eigvalsh(A)[::-1])

    print("\nSINGULAR VALUE DECOMPOSITION")
    U, S, VT = jacobi_svd(A)

    print("Singular values:", S)
    print("Reconstruction error:",
          np.linalg.norm(A - U @ np.diag(S) @ VT))
    assert np.allclose(U @ np.diag(S) @ VT, A)

    print("\nPSEUDOINVERSE")
    print(pseudoinverse(A))
    assert np.allclose(pseudoinverse(A), np.linalg.inv(A))

    print("\nLEAST SQUARES")
    print(least_squares(A, b))
    assert np.allclose(least_squares(A, b), np.linalg.solve(A, b))

    print("\nCONJUGATE GRADIENT")
    solution, iterations = conjugate_gradient(A, b)

    print("Solution:", solution)
    print("Iterations:", iterations)
    assert np.allclose(A @ solution, b)

    print("\nPOWER ITERATION")
    print(power_iteration(A))
    assert np.isclose(power_iteration(A)[0], np.linalg.eigvalsh(A).max())

    print("\nINVERSE POWER ITERATION")
    lam, _ = inverse_power_iteration(A)
    print(lam)
    assert np.isclose(lam, np.linalg.eigvalsh(A).min())

    print("\nGRAM-SCHMIDT")
    G = gram_schmidt(A)
    print(G)
    assert np.allclose(G.T @ G, np.eye(3))

    print("\nCONDITION NUMBER")
    print(condition_number(A))
    assert np.isclose(condition_number(A), np.linalg.cond(A))

    print("\nCHOLESKY")
    L = cholesky_decomposition(A)
    print(L)
    assert np.allclose(L @ L.T, A)

    print("\nAll self-checks passed.")
