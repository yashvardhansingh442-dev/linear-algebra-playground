def matrix_add(A, B):
    """Add two matrices of same dimensions."""
    rows = len(A)
    cols = len(A[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] + B[i][j]
    return result

def matrix_subtract(A, B):
    """Subtract matrix B from matrix A."""
    rows = len(A)
    cols = len(A[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            result[i][j] = A[i][j] - B[i][j]
    return result

# Test
if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    
    print("Addition:", matrix_add(A, B))
    print("Subtraction:", matrix_subtract(A, B))
    
    import numpy as np
    print("NumPy check (add):", np.add(A, B).tolist())
