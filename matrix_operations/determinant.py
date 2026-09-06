def _validate_square(M):
    """Validate that M is a non-empty, rectangular, square matrix. Returns size n."""
    if not M:
        raise ValueError("Matrix cannot be empty.")
    if any(len(row) != len(M[0]) for row in M):
        raise ValueError("Matrix is not rectangular.")
    rows = len(M)
    cols = len(M[0])
    if rows != cols:
        raise ValueError(f"Determinant requires a square matrix, got {rows}x{cols}.")
    return rows


def get_minor(M, i, j):
    """Return the minor of M with row i and column j removed."""
    return [
        [M[row][col] for col in range(len(M)) if col != j]
        for row in range(len(M)) if row != i
    ]


def determinant(M):
    """
    Compute the determinant of a square matrix using cofactor expansion
    along the first row.

    Base cases:
        1x1 -> the single entry
        2x2 -> ad - bc
    Recursive case:
        det(M) = sum over j of (-1)^j * M[0][j] * det(minor(M, 0, j))
    """
    n = _validate_square(M)

    # Base case: 1x1 matrix
    if n == 1:
        return M[0][0]

    # Base case: 2x2 matrix
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]

    # Recursive case: cofactor expansion along the first row
    det = 0
    for j in range(n):
        sign = (-1) ** j
        minor = get_minor(M, 0, j)
        det += sign * M[0][j] * determinant(minor)
    return det


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    A = [
        [1, 2],
        [3, 4]
    ]
    B = [
        [6, 1, 1],
        [4, -2, 5],
        [2, 8, 7]
    ]
    C = [
        [2, 0, 0, 1],
        [1, 3, 0, 0],
        [0, 1, 2, 0],
        [1, 0, 1, 4]
    ]

    for name, M in [("A (2x2)", A), ("B (3x3)", B), ("C (4x4)", C)]:
        print(f"Matrix {name}:")
        for row in M:
            print(row)
        result = determinant(M)
        print(f"Determinant: {result}")

        try:
            import numpy as np
            numpy_result = round(np.linalg.det(M))
            print(f"NumPy Check: {numpy_result}")
            print("Results Match:", result == numpy_result)
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

    # Non-square matrix should raise
    try:
        determinant([[1, 2, 3], [4, 5, 6]])
        print("ERROR: should have raised")
    except ValueError as e:
        print("Raised correctly:", e)
