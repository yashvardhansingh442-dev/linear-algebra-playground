<<<<<<< HEAD
from .utils import as_matrix, shape, print_matrix


def _check_same_shape(A, B, op):
    A = as_matrix(A, "Matrix A")
    B = as_matrix(B, "Matrix B")
    if shape(A) != shape(B):
        ra, ca = shape(A)
        rb, cb = shape(B)
        raise ValueError(f"Cannot {op} a {ra}x{ca} matrix and a {rb}x{cb} matrix.")
    return A, B


def matrix_add(A, B):
    """Add two matrices of the same dimensions: (A + B)[i][j] = A[i][j] + B[i][j]."""
    A, B = _check_same_shape(A, B, "add")
    rows, cols = shape(A)
    return [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]


def matrix_subtract(A, B):
    """Subtract B from A: (A - B)[i][j] = A[i][j] - B[i][j]."""
    A, B = _check_same_shape(A, B, "subtract")
    rows, cols = shape(A)
    return [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]


# ---------------------- TEST ----------------------
if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    print_matrix(matrix_add(A, B), "Addition")
    print_matrix(matrix_subtract(A, B), "Subtraction")

    try:
        import numpy as np
        print("NumPy check (add):", np.add(A, B).tolist())
        print("NumPy check (subtract):", np.subtract(A, B).tolist())
    except ImportError:
        print("NumPy is not installed. Skipping verification.")

    try:
        matrix_add([[1, 2]], [[1], [2]])
        print("ERROR: should have raised")
    except ValueError as e:
        print("Raised correctly:", e)
=======
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
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
