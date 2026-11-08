import numpy as np
from scipy.linalg import lu, lu_factor, lu_solve

A = np.array([[2,1,1],
              [4,-6,0],
              [-2,7,2]], dtype=float)
b = np.array([5,-2,9], dtype=float)

P, L, U = lu(A)
print("P:\n", P)
print("L:\n", L)
print("U:\n", U)
print("Check PA = LU:\n", P @ A, "\n", L @ U)

# Solve via forward + back substitution manually
c = np.linalg.solve(L, P @ b)   # forward substitution
x = np.linalg.solve(U, c)       # back substitution
print(x)                        # [1. 1. 2.]

# Reuse the same factorization for a different b (the efficiency payoff)
lu_piv = lu_factor(A)
b2 = np.array([1, 2, 3], dtype=float)
x2 = lu_solve(lu_piv, b2)
print(x2)

# Row exchange example
A2 = np.array([[0,1],[2,3]], dtype=float)
P2, L2, U2 = lu(A2)
print(P2, "\n", L2, "\n", U2)
