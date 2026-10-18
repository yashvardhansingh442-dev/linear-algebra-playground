from .utils import as_square_matrix, identity, pivot_tolerance, print_matrix


def inverse(A, tol=None):
    """
    Invert a square matrix with Gauss-Jordan elimination.

    Build the augmented matrix [A | I] and use row operations (with partial
    pivoting) to reduce the left half to the identity. Whatever has happened
    to the right half by then is A^-1.

    Singularity is detected from the pivots themselves: if no usable pivot
    (magnitude > tol, default n * eps * max|a_ij|) exists in a column, A is
    not invertible and a ValueError is raised. This is O(n^3), unlike
    checking det(A) == 0 via cofactor expansion, which is O(n!) *and*
    fragile with floating point.
    """
    A = as_square_matrix(A, "Inversion")
    n = len(A)
    eps = pivot_tolerance(A, tol)

    I = identity(n)
    aug = [[float(x) for x in A[i]] + I[i] for i in range(n)]

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) <= eps:
            raise ValueError("Matrix is singular; it has no inverse.")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # Scale the pivot row so the pivot becomes exactly 1
        pivot = aug[col][col]
        aug[col] = [x / pivot for x in aug[col]]

        # Clear this column in every *other* row (above and below)
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                if factor != 0:
                    aug[row] = [aug[row][k] - factor * aug[col][k] for k in range(2 * n)]

    return [row[n:] for row in aug]


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    from .multiplication import matrix_multiply

    examples = [
        ("A (2x2)", [[2, 1], [1, 1]]),
        ("B (3x3, needs a row swap)", [[0, 2, 1], [1, 1, 0], [2, 0, 3]]),
        ("K (second-difference matrix)", [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]),
    ]

    for name, M in examples:
        print_matrix(M, f"Matrix {name}")
        inv = inverse(M)
        print_matrix(inv, "Inverse")
        print_matrix(matrix_multiply(M, inv), "A @ A^-1 (should be the identity)")
        try:
            import numpy as np
            print("Matches np.linalg.inv:", np.allclose(inv, np.linalg.inv(M)))
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

    try:
        inverse([[1, 2], [2, 4]])
        print("ERROR: should have raised")
    except ValueError as e:
        print("Raised correctly:", e)
