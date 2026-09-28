import numpy as np

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[0, 1],
              [1, 0]])
x = np.array([5, 6])

print(A + B)          # [[1 3] [4 4]]
print(2 * A)          # [[2 4] [6 8]]
print(A.T)            # [[1 3] [2 4]]
print(A @ x)          # [17 39]
print(A @ B)          # [[2 1] [4 3]]
print(B @ A)          # [[3 4] [1 2]]  <- different from A @ B
print(A * B)          # [[0 2] [3 0]]  <- element-wise, NOT matrix multiplication
print(np.eye(2))      # identity

# Rotation
theta = np.radians(90)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
print(np.round(R @ np.array([1, 0]), 6))   # [0. 1.]

# Composition: rotate first, then scale
S = np.array([[2, 0],
              [0, 3]])
print(np.round(S @ R, 6))                  # [[ 0. -2.] [ 3.  0.]]

# Shape checking
C = np.array([[1, 0, 2],
              [0, 1, 3]])   # 2x3
D = np.array([[1, 2],
              [3, 4],
              [5, 6]])      # 3x2
print(C.shape, D.shape, (C @ D).shape)     # (2,3) (3,2) (2,2)
