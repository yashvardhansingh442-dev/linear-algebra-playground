import numpy as np

A = np.array([[2, -1],
              [1, 1]], dtype=float)
b = np.array([1, 5], dtype=float)
x = np.linalg.solve(A, b)
print(x)   # [2. 3.]

# Verify the column picture directly
col1, col2 = A[:,0], A[:,1]
check = x[0]*col1 + x[1]*col2
print(check)   # [1. 5.] matches b

# 3D example
A3 = np.array([[2,1,1],
               [4,-6,0],
               [-2,7,2]], dtype=float)
b3 = np.array([5,-2,9], dtype=float)
print(np.linalg.solve(A3, b3))   # [1. 1. 2.]

# Singular example
S = np.array([[1,2],[2,4]], dtype=float)
print(np.linalg.det(S))          # 0.0 -> singular, columns are parallel
