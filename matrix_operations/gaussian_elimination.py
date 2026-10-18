<<<<<<< HEAD
from .utils import as_matrix, as_vector, shape, pivot_tolerance, print_matrix


def _validate_system(A, b):
    """Validate Ax = b (A square, len(b) == rows of A). Returns (A, b, n)."""
    A = as_matrix(A, "Matrix A")
    b = as_vector(b, "Vector b")
    rows_A, cols_A = shape(A)
=======
def _validate_system(A, b):
    """Validate A is square/rectangular and b matches A's row count. Returns n."""
    if not A or not b:
        raise ValueError("A and b cannot be empty.")
    if any(len(row) != len(A[0]) for row in A):
        raise ValueError("Matrix A is not rectangular.")

    rows_A = len(A)
    cols_A = len(A[0])

>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
    if rows_A != cols_A:
        raise ValueError(f"Gaussian elimination here requires a square A, got {rows_A}x{cols_A}.")
    if len(b) != rows_A:
        raise ValueError(f"b has {len(b)} entries but A has {rows_A} rows.")
<<<<<<< HEAD
    return A, b, rows_A


def forward_elimination(A, b, tol=None):
    """
    Reduce [A | b] to row echelon form using partial pivoting.
    Returns the augmented matrix in echelon form (list of lists, each of length n+1).

    A pivot whose magnitude is <= `tol` (default: n * eps * max|a_ij|) counts
    as zero, so numerically singular systems are rejected instead of
    silently producing huge garbage values.
    """
    A, b, n = _validate_system(A, b)
    eps = pivot_tolerance(A, tol)

    # Build augmented matrix [A | b] so we don't mutate the caller's data
    aug = [[float(x) for x in A[i]] + [float(b[i])] for i in range(n)]

    for col in range(n):
        # Partial pivoting: find the row with the largest entry in this column
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))

        if abs(aug[pivot_row][col]) <= eps:
=======
    return rows_A


def forward_elimination(A, b):
    """
    Reduce [A | b] to row echelon form using partial pivoting.
    Returns the augmented matrix in echelon form (list of lists, each of length n+1).
    """
    n = _validate_system(A, b)

    # Build augmented matrix [A | b] so we don't mutate the caller's data
    aug = [list(A[i]) + [b[i]] for i in range(n)]

    for col in range(n):
        # Partial pivoting: find the row with the largest entry in this column
        pivot_row = col
        for row in range(col, n):
            if abs(aug[row][col]) > abs(aug[pivot_row][col]):
                pivot_row = row

        if aug[pivot_row][col] == 0:
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
            raise ValueError("Matrix is singular; system has no unique solution.")

        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # Eliminate this column from every row below the pivot
        for row in range(col + 1, n):
            factor = aug[row][col] / aug[col][col]
            aug[row] = [aug[row][k] - factor * aug[col][k] for k in range(n + 1)]

    return aug


def back_substitution(aug):
    """
    Solve for x given an augmented matrix already in row echelon form.
    """
    n = len(aug)
<<<<<<< HEAD
    x = [0.0] * n
=======
    x = [0] * n
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

    for i in range(n - 1, -1, -1):
        total = aug[i][n]
        for j in range(i + 1, n):
            total -= aug[i][j] * x[j]
        x[i] = total / aug[i][i]

    return x


<<<<<<< HEAD
def solve(A, b, tol=None):
=======
def solve(A, b):
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
    """
    Solve the system Ax = b using Gaussian elimination:
    forward elimination to row echelon form, then back-substitution.
    """
<<<<<<< HEAD
    aug = forward_elimination(A, b, tol)
=======
    aug = forward_elimination(A, b)
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
    return back_substitution(aug)


# ---------------------- TEST ----------------------
if __name__ == "__main__":
<<<<<<< HEAD
    systems = [
        ("3x3 system", [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]),
        ("2x2 system", [[3, 2], [1, 4]], [5, 6]),
        ("needs a row swap (zero in the top-left pivot)", [[0, 1], [1, 0]], [2, 3]),
    ]

    for label, A, b in systems:
        print_matrix(A, f"{label}: matrix A")
        print("Vector b:", b)
        x = solve(A, b)
        print("Solution x:", [round(val, 4) for val in x])
        try:
            import numpy as np
            numpy_x = np.linalg.solve(A, b)
            print("NumPy Check:", [round(float(val), 4) for val in numpy_x])
            print("Results Match:", np.allclose(x, numpy_x))
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

    # Singular systems should raise -- including *numerically* singular ones
    for label, A, b in [
        ("exactly singular", [[1, 2], [2, 4]], [3, 6]),
        ("numerically singular", [[1, 2], [1, 2.0000000000000004]], [3, 6]),
    ]:
        try:
            solve(A, b)
            print("ERROR: should have raised")
        except ValueError as e:
            print(f"Raised correctly ({label}):", e)
=======
    A = [
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ]
    b = [8, -11, -3]

    print("Matrix A:")
    for row in A:
        print(row)
    print("Vector b:", b)

    x = solve(A, b)
    print("\nSolution x:", [round(val, 4) for val in x])

    try:
        import numpy as np
        numpy_x = np.linalg.solve(A, b)
        print("NumPy Check:", [round(val, 4) for val in numpy_x])
        print("Results Match:", np.allclose(x, numpy_x))
    except ImportError:
        print("NumPy is not installed. Skipping verification.")

    # Second example: 2x2 system
    A2 = [
        [3, 2],
        [1, 4]
    ]
    b2 = [5, 6]

    print("\nMatrix A2:")
    for row in A2:
        print(row)
    print("Vector b2:", b2)

    x2 = solve(A2, b2)
    print("Solution x2:", [round(val, 4) for val in x2])

    try:
        import numpy as np
        numpy_x2 = np.linalg.solve(A2, b2)
        print("NumPy Check:", [round(val, 4) for val in numpy_x2])
        print("Results Match:", np.allclose(x2, numpy_x2))
    except ImportError:
        pass

    # Singular system should raise
    try:
        solve([[1, 2], [2, 4]], [3, 6])
        print("ERROR: should have raised")
    except ValueError as e:
        print("\nRaised correctly:", e)
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
