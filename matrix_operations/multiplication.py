def _validate(A, B):
    """Shared validation for all multiplication views. Returns dimensions."""
    # Check for empty matrices
    if not A or not B:
        raise ValueError("Matrices cannot be empty.")
    # Check that all rows have the same length
    if any(len(row) != len(A[0]) for row in A):
        raise ValueError("Matrix A is not rectangular.")
    if any(len(row) != len(B[0]) for row in B):
        raise ValueError("Matrix B is not rectangular.")

    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check matrix dimensions
    if cols_A != rows_B:
        raise ValueError(
            f"Cannot multiply a {rows_A}x{cols_A} matrix "
            f"with a {rows_B}x{cols_B} matrix."
        )
    return rows_A, cols_A, rows_B, cols_B


def matrix_multiply(A, B):
    """
    Multiply two matrices using the standard row·column dot-product view.
    A: m x n matrix
    B: n x p matrix
    Returns:
        m x p matrix
    """
    rows_A, cols_A, rows_B, cols_B = _validate(A, B)

    # Initialize result matrix with zeros
    result = [[0] * cols_B for _ in range(rows_A)]

    # Matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            total = 0
            for k in range(cols_A):
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result


def matrix_multiply_columns(A, B):
    """
    Column-picture view: each column of AB is a linear combination of
    the columns of A, weighted by the corresponding column of B.

    column_j(AB) = B[0][j]*col_0(A) + B[1][j]*col_1(A) + ... + B[n-1][j]*col_{n-1}(A)
    """
    rows_A, cols_A, rows_B, cols_B = _validate(A, B)

    result = [[0] * cols_B for _ in range(rows_A)]

    for j in range(cols_B):
        combo = [0] * rows_A
        for k in range(cols_A):
            weight = B[k][j]
            for i in range(rows_A):
                combo[i] += A[i][k] * weight
        for i in range(rows_A):
            result[i][j] = combo[i]
    return result


def matrix_multiply_rows(A, B):
    """
    Row-picture view: each row of AB is a linear combination of
    the rows of B, weighted by the corresponding row of A.

    row_i(AB) = A[i][0]*row_0(B) + A[i][1]*row_1(B) + ... + A[i][n-1]*row_{n-1}(B)
    """
    rows_A, cols_A, rows_B, cols_B = _validate(A, B)

    result = [[0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        combo = [0] * cols_B
        for k in range(cols_A):
            weight = A[i][k]
            for j in range(cols_B):
                combo[j] += weight * B[k][j]
        result[i] = combo
    return result


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    A = [
        [1, 2],
        [3, 4]
    ]
    B = [
        [5, 6],
        [7, 8]
    ]

    dot_result = matrix_multiply(A, B)
    col_result = matrix_multiply_columns(A, B)
    row_result = matrix_multiply_rows(A, B)

    print("Matrix A:")
    for row in A:
        print(row)
    print("\nMatrix B:")
    for row in B:
        print(row)

    print("\nDot-product view result:")
    for row in dot_result:
        print(row)

    print("\nColumn-picture view result:")
    for row in col_result:
        print(row)

    print("\nRow-picture view result:")
    for row in row_result:
        print(row)

    print("\nAll views agree:", dot_result == col_result == row_result)

    # NumPy verification (optional)
    try:
        import numpy as np
        numpy_result = np.matmul(A, B).tolist()
        print("\nNumPy Check:")
        for row in numpy_result:
            print(row)
        print("\nResults Match:", dot_result == numpy_result)
    except ImportError:
        print("\nNumPy is not installed. Skipping verification.")
