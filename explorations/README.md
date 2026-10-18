# Explorations

Short NumPy / SciPy scripts used to *see* an idea before (or after) implementing
it by hand in [`matrix_operations/`](../matrix_operations). Unlike the core
modules, these deliberately lean on `numpy.linalg` and `scipy.linalg` -- they are
experiments, not from-scratch implementations.

| Script | What it explores |
|--------|------------------|
| `vectors.py` | Vector arithmetic, dot product, norm, angle between vectors |
| `matrices.py` | Matrix arithmetic, non-commutativity, rotation/scaling, shape rules |
| `linear_system.py` | Unique / inconsistent systems and rank |
| `column_space_and_singularity.py` | Column picture of `Ax = b`, singular matrices |
| `elimination_and_matrix_factorization.py` | Step-by-step elimination, LU, outer-product view of `AB` |
| `lu_decomposition.py` | `PA = LU`, reusing a factorization for many right-hand sides |
| `inverse_properties.py` | Gauss-Jordan by hand on a 2x2, `(AB)^-1 = B^-1 A^-1`, `A^T A` symmetry |
| `ldl_and_conditioning.py` | `LDL^T`, dense vs. tridiagonal solves, Hilbert-matrix conditioning |
| `solver_benchmark.py` | Dense, LU, Cholesky, sparse and CG solvers compared on accuracy and speed |

Run any of them directly, e.g. `python explorations/lu_decomposition.py`.
Requires `numpy` and `scipy` (`pip install -r requirements.txt`).
