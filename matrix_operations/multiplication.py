def matrix_multiply(A, B):
    """Multiply two matrices: A (m x n) * B (n x p) = result (m x p)"""
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions don't match for multiplication")
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Test
if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    
    print("Multiplication:", matrix_multiply(A, B))
    
    import numpy as np
    print("NumPy check:", np.matmul(A, B).tolist())
