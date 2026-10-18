<<<<<<< HEAD
from .utils import as_square_matrix, pivot_tolerance, print_matrix
=======
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
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681


def get_minor(M, i, j):
    """Return the minor of M with row i and column j removed."""
    return [
        [M[row][col] for col in range(len(M)) if col != j]
        for row in range(len(M)) if row != i
    ]


<<<<<<< HEAD
def _cofactor_det(M):
    """Recursive cofactor expansion on an already-validated square matrix."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    det = 0
    for j in range(n):
        det += (-1) ** j * M[0][j] * _cofactor_det(get_minor(M, 0, j))
    return det


=======
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
def determinant(M):
    """
    Compute the determinant of a square matrix using cofactor expansion
    along the first row.

    Base cases:
        1x1 -> the single entry
        2x2 -> ad - bc
    Recursive case:
        det(M) = sum over j of (-1)^j * M[0][j] * det(minor(M, 0, j))
<<<<<<< HEAD

    Exact for integer input, but O(n!) -- see determinant_elimination for
    the O(n^3) alternative.
    """
    M = as_square_matrix(M, "Determinant")
    return _cofactor_det(M)


def determinant_elimination(M, tol=None):
    """
    Determinant via forward elimination with partial pivoting: O(n^3).

    Reduce M to upper-triangular form U; then det(M) is the product of the
    pivots, times -1 for every row swap. If a column has no usable pivot
    (all entries below the tolerance), the matrix is singular and the
    determinant is 0.0.
    """
    A = as_square_matrix(M, "Determinant")
    A = [[float(x) for x in row] for row in A]
    n = len(A)
    eps = pivot_tolerance(A, tol)
    sign = 1.0
    det = 1.0

    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[pivot_row][col]) <= eps:
            return 0.0
        if pivot_row != col:
            A[col], A[pivot_row] = A[pivot_row], A[col]
            sign = -sign
        det *= A[col][col]
        for row in range(col + 1, n):
            factor = A[row][col] / A[col][col]
            for k in range(col, n):
                A[row][k] -= factor * A[col][k]

    return sign * det
=======
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
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681


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
<<<<<<< HEAD
        print_matrix(M, f"Matrix {name}")
        result = determinant(M)
        fast = determinant_elimination(M)
        print(f"Determinant (cofactor):     {result}")
        print(f"Determinant (elimination):  {round(fast, 10)}")

        try:
            import numpy as np
            numpy_result = np.linalg.det(M)
            print(f"NumPy Check:                {round(float(numpy_result), 10)}")
            print("Results Match:", abs(result - numpy_result) < 1e-9
                  and abs(fast - numpy_result) < 1e-9)
=======
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
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
        except ImportError:
            print("NumPy is not installed. Skipping verification.")
        print()

<<<<<<< HEAD
    # Singular matrix: rows 1 and 2 are proportional
    print("det of singular [[1,2],[2,4]]:",
          determinant([[1, 2], [2, 4]]), "/", determinant_elimination([[1, 2], [2, 4]]))

=======
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
    # Non-square matrix should raise
    try:
        determinant([[1, 2, 3], [4, 5, 6]])
        print("ERROR: should have raised")
    except ValueError as e:
        print("Raised correctly:", e)
