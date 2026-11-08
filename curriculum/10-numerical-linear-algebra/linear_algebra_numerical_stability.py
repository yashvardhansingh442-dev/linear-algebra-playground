
import time
import numpy as np
from scipy.linalg import lu_factor, lu_solve, cho_factor, cho_solve
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve, cg


def build_spd_matrix(n):
    """Build a symmetric positive-definite tridiagonal matrix."""
    diagonal = 2.0 * np.ones(n)
    off_diagonal = -1.0 * np.ones(n - 1)

    return diags(
        [off_diagonal, diagonal, off_diagonal],
        offsets=[-1, 0, 1],
        format="csr"
    )


def relative_residual(A, x, b):
    """Measure how accurately Ax = b is satisfied."""
    numerator = np.linalg.norm(A @ x - b)
    denominator = np.linalg.norm(b)

    return numerator / denominator if denominator else numerator


def benchmark(name, solver, A, b):
    """Time a solver and evaluate its numerical accuracy."""
    start = time.perf_counter()
    x = solver()
    elapsed = time.perf_counter() - start

    error = relative_residual(A, x, b)

    return {
        "method": name,
        "solution": x,
        "time": elapsed,
        "residual": error
    }


def main():
    n = 300

    # Construct a sparse SPD matrix and a known solution.
    A_sparse = build_spd_matrix(n)
    x_true = np.sin(np.linspace(0, 2 * np.pi, n))
    b = A_sparse @ x_true

    # Dense representation for dense direct solvers.
    A_dense = A_sparse.toarray()

    # Factorize once, then solve.
    lu, piv = lu_factor(A_dense)
    chol, lower = cho_factor(A_dense)

    methods = [
        (
            "NumPy solve",
            lambda: np.linalg.solve(A_dense, b),
            A_dense
        ),
        (
            "SciPy LU",
            lambda: lu_solve((lu, piv), b),
            A_dense
        ),
        (
            "Cholesky",
            lambda: cho_solve((chol, lower), b),
            A_dense
        ),
        (
            "Sparse direct",
            lambda: spsolve(A_sparse, b),
            A_sparse
        ),
        (
            "Conjugate gradient",
            lambda: cg(
                A_sparse, b,
                rtol=1e-10,
                atol=0.0,
                maxiter=10 * n
            )[0],
            A_sparse
        ),
    ]

    print(f"Matrix size: {n} x {n}")
    print(f"Nonzero entries: {A_sparse.nnz}")
    print(f"Condition number: {np.linalg.cond(A_dense):.4e}")
    print("-" * 76)
    print(f"{'Method':<23} {'Time (s)':>12} {'Residual':>18} {'Solution error':>18}")
    print("-" * 76)

    results = []

    for name, solver, matrix in methods:
        result = benchmark(name, solver, matrix, b)

        solution_error = (
            np.linalg.norm(result["solution"] - x_true)
            / np.linalg.norm(x_true)
        )

        results.append(result)

        print(
            f"{name:<23} "
            f"{result['time']:>12.6f} "
            f"{result['residual']:>18.4e} "
            f"{solution_error:>18.4e}"
        )

    print("-" * 76)

    # Check the best numerical accuracy.
    best = min(results, key=lambda r: r["residual"])
    print(f"Lowest residual: {best['method']}")
    print(f"Residual value:  {best['residual']:.4e}")


if __name__ == "__main__":
    main()
