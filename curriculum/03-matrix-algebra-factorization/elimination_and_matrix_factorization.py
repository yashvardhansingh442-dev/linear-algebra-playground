import numpy as np

A = np.array([[2,1,1],
              [4,-6,0],
              [-2,7,2]], dtype=float)
b = np.array([5,-2,9], dtype=float)

# Manual elimination, step by step
M = np.hstack([A, b.reshape(-1,1)])
print("Start:\n", M)

M[1] = M[1] - 2*M[0]
M[2] = M[2] + 1*M[0]
print("After step 1:\n", M)

M[2] = M[2] + 1*M[1]
print("After step 2 (upper triangular):\n", M)

# scipy gives LU directly
from scipy.linalg import lu
P, L, U = lu(A)
print("L:\n", L)
print("U:\n", U)

# Four views of multiplication
A2 = np.array([[1,2],[3,4]])
B2 = np.array([[0,1],[1,2]])
print(A2 @ B2)                                   # standard

# outer product sum
outer_sum = np.outer(A2[:,0], B2[0,:]) + np.outer(A2[:,1], B2[1,:])
print(outer_sum)                                 # matches A2 @ B2
