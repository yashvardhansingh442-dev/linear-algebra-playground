<div align="center">

# Linear Algebra Playground

**Core linear algebra, built by hand in pure Python and checked against NumPy.**

[![CI](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml/badge.svg)](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/runtime%20dependencies-none-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

A study project built while working through Gilbert Strang's *Introduction to Linear Algebra* (MIT 18.06). Each algorithm is written with plain Python lists and loops, with no `numpy.linalg` and no NumPy at all in the library code. NumPy and SciPy are used only to **verify** the results, in the tests and in the demo at the bottom of each module.

If you are working through 18.06 yourself, every module doubles as a worked example: run it and it prints its steps and compares its answer with NumPy.

## Contents

- [Quick start](#quick-start)
- [What's implemented](#whats-implemented)
- [API reference](#api-reference)
- [How the algorithms work](#how-the-algorithms-work)
- [Testing](#testing)
- [Project layout](#project-layout)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Contributing, source and license](#contributing-source-and-license)

---

## Quick start

**Install** (Python 3.10 or newer):

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
pip install -e ".[dev]"      # the library plus numpy, scipy and pytest
```

The library itself needs nothing beyond the standard library. The `dev` extra is only for tests and the NumPy cross-checks.

**Use it:**

```python
from linalg.core.multiplication import matrix_multiply
from linalg.core.determinant import determinant, determinant_elimination
from linalg.solvers.gaussian_elimination import solve
from linalg.solvers.matrix_inverse import inverse
from linalg.decompositions.eigen import eigen, power_iteration

A = [[2, 1], [1, 3]]

matrix_multiply(A, A)        # [[5, 5], [5, 10]]
determinant(A)               # 5
solve(A, [1, 2])             # [0.2, 0.6]
inverse(A)                   # [[0.6, -0.2], [-0.2, 0.4]]
eigen(A)                     # ([1.382, 3.618], [[...], [...]])  values ascending, unit vectors
power_iteration(A)           # (3.618, [...])                    dominant eigenpair
```

**Watch a worked example.** Every module has a demo that prints its steps and checks them against NumPy. Run it with `-m`, because the modules use relative imports:

```bash
python -m linalg.core.addition_subtraction
python -m linalg.core.multiplication
python -m linalg.core.determinant
python -m linalg.solvers.gaussian_elimination
python -m linalg.solvers.matrix_inverse
python -m linalg.decompositions.eigen
```

**Run the tests:**

```bash
pytest                  # everything
pytest -k eigen         # one module
make check              # lint, format check, type check and tests (what CI runs)
```

---

## What's implemented

| Topic | Module | Strang lecture |
|-------|--------|----------------|
| Matrix addition and subtraction | `core/addition_subtraction.py` | 1 |
| Matrix multiplication (dot-product, row and column views) | `core/multiplication.py` | 1-3 |
| Determinants (cofactor expansion and O(n³) elimination) | `core/determinant.py` | 18-19 |
| Gaussian elimination (`Ax = b`) | `solvers/gaussian_elimination.py` | 2 |
| Matrix inverse (Gauss-Jordan) | `solvers/matrix_inverse.py` | 3 |
| Eigenvalues and eigenvectors | `decompositions/eigen.py` | 21-22 |

All modules live in `src/linalg/`. Shared validation, tolerances and printing helpers are in `core/utils.py`, and `eigen.py` builds on `determinant.py`.

---

## API reference

Every public function accepts matrices as lists of lists (NumPy arrays are converted), never modifies its input, and returns plain Python lists and floats. Bad input raises `ValueError` with a specific message.

### `core/utils.py`

| Function | Purpose |
|----------|---------|
| `as_matrix(M, name)` / `as_vector(v, name)` | Validate and copy. Rejects empty, ragged, non-numeric and NaN/inf input. |
| `as_square_matrix(M, operation, name)` | `as_matrix` plus a square check. |
| `shape(M)`, `identity(n)` | Dimensions and the `n × n` identity. |
| `pivot_tolerance(M, tol=None)` | The "is this pivot zero?" threshold: `n · ε · max\|aᵢⱼ\|`, or `tol` if given. |
| `mat_vec(A, v)`, `norm(v)`, `max_abs(M)` | Small numeric helpers. |
| `print_matrix(M, name=None, precision=4)` | One row per line. |

### `core/addition_subtraction.py`

| Function | Returns |
|----------|---------|
| `matrix_add(A, B)` | `A + B`; `ValueError` if the shapes differ |
| `matrix_subtract(A, B)` | `A − B`; same |

### `core/multiplication.py`

Three views of one product. For `A (m × n)` and `B (n × p)` each returns an `m × p` matrix, and raises `ValueError` if the inner dimensions differ.

| Function | View |
|----------|------|
| `matrix_multiply(A, B)` | Entry `(i, j)` is row *i* of A dotted with column *j* of B. |
| `matrix_multiply_columns(A, B)` | Column *j* of AB is a combination of A's **columns**, weighted by column *j* of B. |
| `matrix_multiply_rows(A, B)` | Row *i* of AB is a combination of B's **rows**, weighted by row *i* of A. |

### `core/determinant.py`

| Function | Method | Cost |
|----------|--------|------|
| `determinant(M)` | Cofactor expansion along row 0; exact for integers | O(n!) |
| `determinant_elimination(M, tol=None)` | Partial-pivot elimination; product of pivots times (−1)^swaps; `0.0` if singular | O(n³) |
| `get_minor(M, i, j)` | `M` without row *i* and column *j* | n/a |

### `solvers/gaussian_elimination.py`

| Function | Purpose |
|----------|---------|
| `solve(A, b, tol=None)` | Solve `Ax = b` for square, non-singular `A`. |
| `forward_elimination(A, b, tol=None)` | Reduce `[A \| b]` to row echelon form with partial pivoting. |
| `back_substitution(aug)` | Solve from the bottom row up. |

Raises `ValueError` for non-square `A`, a mismatched `b`, or a singular or numerically singular system.

### `solvers/matrix_inverse.py`

| Function | Purpose |
|----------|---------|
| `inverse(A, tol=None)` | Gauss-Jordan inverse via `[A \| I] → [I \| A⁻¹]`. `ValueError` if `A` is singular or not square. |

### `decompositions/eigen.py`

| Function | Purpose |
|----------|---------|
| `characteristic_polynomial(A)` | Coefficients `[1, −tr(A), …]`, highest power first, for 2×2 and 3×3. |
| `eigenvalues(A)` | Real eigenvalues, ascending, with multiplicity. `ValueError` if any are complex. |
| `eigenspace(A, lam)` | Unit basis vectors of the eigenspace for `lam`. |
| `eigenvector_for(A, lam)` | The first vector of `eigenspace`. |
| `eigen(A)` | `(values, vectors)` where `vectors[i]` is a unit eigenvector for `values[i]`. |
| `power_iteration(A, num_iterations=1000, tol=1e-10, start=None)` | Dominant eigenpair for any square size; warns if it does not converge. |

`eigen` returns a repeated eigenvalue once per independent eigenvector, so **fewer than *n* pairs means the matrix is defective**:

| Matrix | Result |
|--------|--------|
| `[[4, 1], [2, 3]]` (distinct eigenvalues) | 2 eigenvalues, 2 eigenvectors |
| `I₃` (repeated, full eigenspace) | `[1, 1, 1]` with three different eigenvectors |
| `[[2, 1], [0, 2]]` (repeated, defective) | `[2]` with one eigenvector, so not diagonalizable |

---

## How the algorithms work

**Multiplication has three faces.** The dot-product definition is the one most people learn. The column picture says each column of `AB` is a combination of the columns of `A`, which is the idea that later explains column space and rank. The row picture is the mirror image. All three give identical results, and the tests check that they agree.

**Determinants, two ways.** Cofactor expansion, `det(A) = Σ (−1)^j · A[0][j] · det(minor)`, shows the definition directly but costs O(n!). Elimination reduces to an upper-triangular `U` and multiplies the pivots, flipping the sign for each row swap. The two agree, which links "the formula" to "the pivots".

**Elimination and inverses share one engine.** `solve` runs forward elimination with partial pivoting (swap in the row with the largest entry in the column), then back-substitutes. `inverse` is the same machinery applied to `[A | I]`, so it solves `n` systems at once. Singularity is detected from the pivots, not from `det(A) == 0`, which would be O(n!) and unreliable in floating point.

**Tolerances, never `== 0`.** A pivot counts as zero when its magnitude is at most `n · ε · max|aᵢⱼ|` (ε ≈ 2.2·10⁻¹⁶), the same idea LAPACK and NumPy's `matrix_rank` use. This rejects `[[1, 2], [1, 2.0000000000000004]]` as singular while still solving an ill-conditioned but invertible Hilbert system. Pass `tol=` to override.

**Eigenvalues, two complementary routes.**
- *Exact (2×2 and 3×3).* The characteristic polynomial is built from trace and determinant identities. The 2×2 case uses the quadratic formula. The 3×3 case uses a hand-written cubic solver driven by the discriminant of the depressed cubic: three distinct real roots use the trigonometric form, a repeated root uses a closed form, and complex roots are rejected.
- *Approximate (any size).* Power iteration applies `A` repeatedly and renormalizes, converging to the dominant eigenvector. The eigenvalue is read off with the Rayleigh quotient, and the loop stops when `‖Av − λv‖` is small.
- *Eigenvectors* come from solving `(A − λI)v = 0` by row reduction, giving one basis vector per free variable.

### Complexity

| Routine | Time | Notes |
|---------|------|-------|
| `matrix_add`, `matrix_subtract` | O(mn) | |
| `matrix_multiply` (all views) | O(mnp) | |
| `determinant` | O(n!) | exact for integers, impractical past about 6×6 |
| `determinant_elimination`, `solve`, `inverse` | O(n³) | partial pivoting |
| `power_iteration` | O(k·n²) | `k` iterations; converges at roughly \|λ₂/λ₁\| per step |

---

## Testing

The suite lives in `tests/unit/` and runs in CI on Python 3.10, 3.11 and 3.12. It checks four things:

1. **Against NumPy.** Seeded random matrices of many sizes are compared with `np.matmul`, `np.linalg.det`, `inv`, `solve` and `eigvalsh`.
2. **Mathematical properties.** `A·A⁻¹ = I`, `(AB)⁻¹ = B⁻¹A⁻¹`, `det(AB) = det(A)·det(B)`, and `Av = λv` for every returned eigenpair.
3. **Hard cases.** Zero pivots that force row swaps, repeated and defective eigenvalues, ill-conditioned Hilbert systems, and numerically singular matrices.
4. **Error paths.** Singular, non-square, ragged, empty, non-finite and complex-eigenvalue inputs must each raise the right error.

A smoke test also runs every script in `explorations/`, so the demos cannot silently break. The `tests/property/` and `tests/numerical/` folders are reserved for Hypothesis and ill-conditioned-matrix tests.

---

## Project layout

```
src/linalg/
├── core/              utils, addition_subtraction, multiplication, determinant
├── solvers/           gaussian_elimination, matrix_inverse
└── decompositions/    eigen
tests/
└── unit/              pytest suite, one file per module
explorations/          NumPy/SciPy experiments (not from-scratch); see its README
curriculum/            lesson-style scripts, organised by topic
resources/             reference material
```

`src/linalg/` is the from-scratch library. `explorations/` is a scratchpad that deliberately uses `numpy.linalg` and `scipy.linalg` to see an idea before or after implementing it by hand.

**Design principles:**
- Manual first: library code uses only lists and loops.
- Fail loudly: validation lives in one place, `core/utils.py`.
- Explicit tolerances that scale with the matrix.
- Never mutate the caller's data.

---

## Limitations

- `determinant()` is O(n!); use `determinant_elimination()` beyond about 6×6.
- Eigenvalues by characteristic polynomial work only for 2×2 and 3×3 (`NotImplementedError` beyond that). `power_iteration` finds only the dominant pair.
- Complex eigenvalues, such as those of a rotation matrix, are not supported and raise `ValueError`.
- The cubic solver treats roots closer than about 10⁻⁶ (relative) as repeated, so nearly defective matrices can lose a few digits.
- Equal-magnitude dominant eigenvalues (for example +1 and −1) stop `power_iteration` from converging. It warns rather than returning a wrong answer.
- Eigenspace bases are not orthogonalised for repeated eigenvalues.
- `solve` needs a square, non-singular `A`.

---

## Roadmap

- [x] Shared validation, tolerances and printing (`utils.py`)
- [x] Test suite against NumPy, with CI
- [x] Determinant by elimination alongside cofactor expansion
- [x] Gauss-Jordan inverse
- [ ] `PA = LU` decomposition (Lecture 4)
- [ ] Reduced row echelon form, rank, and the four fundamental subspaces (Lectures 6-10)
- [ ] Matplotlib visualizations: eigenvector directions, determinant as area
- [ ] QR iteration for general and complex eigenvalues
- [ ] Least squares and SVD

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ImportError: attempted relative import with no known parent package` | You ran a file path. Run it as a module: `python -m linalg.decompositions.eigen`. |
| `ModuleNotFoundError: No module named 'linalg'` | Install the package from the repo root: `pip install -e .` |
| `ModuleNotFoundError: No module named 'numpy'` or `'scipy'` | Only tests and `explorations/` need them: `pip install -e ".[dev]"` |
| `ValueError: Matrix is singular` | `solve` or `inverse` found no usable pivot, so the rows are dependent or nearly so. Lower `tol=` only if you are sure the matrix is merely ill-conditioned. |
| `ValueError` about complex eigenvalues | The matrix has no real eigenvalues (for example a pure rotation). Only the real case is implemented. |
| `eigen()` returns fewer than *n* pairs | Intended: the matrix is defective. See the table under [`decompositions/eigen.py`](#decompositionseigenpy). |
| `RuntimeWarning: power_iteration did not converge` | The two largest eigenvalues are nearly equal in magnitude, or you need more `num_iterations`. |

---

## Contributing, source and license

This is mainly a personal learning log, but bug reports, edge cases and cleaner by-hand derivations are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), run `pytest`, and add a test for anything you fix.

**Learning source:** Gilbert Strang, *Introduction to Linear Algebra* (6th edition), and MIT OpenCourseWare 18.06 Linear Algebra.

**License:** MIT. See [LICENSE](LICENSE).
