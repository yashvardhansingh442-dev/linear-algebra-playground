def matrix_multiply(A, B):
    """
    Multiply two matrices.

    A: m x n matrix
    B: n x p matrix

    Returns:
        m x p matrix
    """

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

    result = matrix_multiply(A, B)

    print("Matrix A:")
    for row in A:
        print(row)

    print("\nMatrix B:")
    for row in B:
        print(row)

    print("\nMultiplication Result:")
    for row in result:
        print(row)

    # NumPy verification (optional)
    try:
        import numpy as np

        numpy_result = np.matmul(A, B).tolist()

        print("\nNumPy Check:")
        for row in numpy_result:
            print(row)

        print("\nResults Match:", result == numpy_result)

    except ImportError:
        print("\nNumPy is not installed. Skipping verification.")
