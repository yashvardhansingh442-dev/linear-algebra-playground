import numpy as np
import time
from scipy.linalg import ldl, hilbert
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# The second-difference matrix K (n = 3)
K = np.array([[ 2,-1, 0],
              [-1, 2,-1],
              [ 0,-1, 2]], dtype=float)

print(np.linalg.det(K))              # 4.0 (product of pivots 2 * 3/2 * 4/3)
print(np.linalg.inv(K) * 4)          # [[3 2 1] [2 4 2] [1 2 3]] -> full inverse

f = np.array([1, 1, 1], dtype=float)
print(np.linalg.solve(K, f))         # [1.5 2.  1.5]

# LDL^T factorization of a symmetric matrix
L, D, perm = ldl(K)
print(L); print(D)
print(np.allclose(L @ D @ L.T, K))   # True

# Cost comparison: dense vs tridiagonal, n = 2000
n = 2000
main = 2*np.ones(n); off = -np.ones(n-1)
K_big_sparse = diags([off, main, off], [-1, 0, 1], format="csc")
K_big_dense  = K_big_sparse.toarray()
f_big = np.ones(n)

t0 = time.time(); np.linalg.solve(K_big_dense, f_big); t_dense = time.time() - t0
t0 = time.time(); spsolve(K_big_sparse, f_big);        t_sparse = time.time() - t0
print(f"dense: {t_dense:.4f}s   sparse: {t_sparse:.6f}s")

# Ill-conditioning: Hilbert matrix
H = hilbert(10)
print(np.linalg.cond(H))             # enormous, roughly 1e13
