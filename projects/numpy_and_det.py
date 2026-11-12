import numpy as np
A = np.array([[1, 2], [4, 5]]); rhs = np.array([3, 6])
print(np.linalg.solve(A, rhs))          # [-1.  2.]
y = (1*6 - 3*4) / (1*5 - 2*4)           # determinant ratio
print(y)                                # 2.0