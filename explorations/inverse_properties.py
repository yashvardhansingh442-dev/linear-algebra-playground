import numpy as np

A = np.array([[2,1],
              [1,1]], dtype=float)

print(np.linalg.inv(A))        # [[ 1. -1.] [-1.  2.]]

# Manual Gauss-Jordan via augmented matrix
aug = np.hstack([A, np.eye(2)])
aug[1] = aug[1] - 0.5*aug[0]
aug[1] = aug[1] / aug[1,1]
aug[0] = aug[0] - aug[0,1]*aug[1]
aug[0] = aug[0] / aug[0,0]
print(aug[:, 2:])              # matches np.linalg.inv(A)

# Singular matrix: Gauss-Jordan can't finish
B = np.array([[1,2],[2,4]], dtype=float)
print(np.linalg.matrix_rank(B))   # 1, not 2 -> no inverse

# (AB)^-1 = B^-1 A^-1
B2 = np.array([[0,1],[1,2]], dtype=float)
lhs = np.linalg.inv(A @ B2)
rhs = np.linalg.inv(B2) @ np.linalg.inv(A)
print(np.allclose(lhs, rhs))      # True

# A^T A is always symmetric, even for non-square A
C = np.array([[1,2,3],[4,5,6]], dtype=float)   # 2x3
S = C.T @ C                                     # 3x3
print(np.allclose(S, S.T))        # True
