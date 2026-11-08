import numpy as np

# Unique solution case
A = np.array([[2, 1],
              [1, -1]], dtype=float)
b = np.array([5, 1], dtype=float)

x = np.linalg.solve(A, b)
print(x)                      # [2. 1.]

# Check rank
print(np.linalg.matrix_rank(A))    # 2 (full rank, unique solution expected)

# 3x3 system
A3 = np.array([[1, 1, 1],
               [0, 2, 5],
               [2, 5, -1]], dtype=float)
b3 = np.array([6, -4, 27], dtype=float)
print(np.linalg.solve(A3, b3))     # [ 5.  3. -2.]

# Inconsistent system: solve() will raise an error
A_bad = np.array([[1, 1],
                   [1, 1]], dtype=float)
b_bad = np.array([2, 5], dtype=float)
print(np.linalg.matrix_rank(A_bad))              # 1
print(np.linalg.matrix_rank(np.column_stack([A_bad, b_bad])))  # 2
# rank(A) < rank([A|b])  ->  no solution. Try np.linalg.solve(A_bad, b_bad) and see it fail.
