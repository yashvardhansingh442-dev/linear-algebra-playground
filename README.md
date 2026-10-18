<div align="center">

# Linear Algebra Playground

**Core linear algebra, implemented by hand in pure Python — verified against NumPy.**

[![CI](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml/badge.svg)](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-134%20passing-brightgreen)
![Status](https://img.shields.io/badge/status-core%20topics%20complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

A from-scratch implementation of core linear algebra algorithms, built while working through **Gilbert Strang's *Introduction to Linear Algebra*** (MIT 18.06). Every algorithm in [`matrix_operations/`](matrix_operations) uses plain Python lists and loops — no `numpy.linalg`, no NumPy at all in the library code. NumPy and SciPy appear only to **check the answers** (in the tests and in each script's demo block) and in the [`explorations/`](explorations) experiments.

If you're also working through 18.06 or Strang's textbook, this repo doubles as a study log: each module runs on its own, prints its work step by step, and states which lecture the concept comes from.

---

## Table of Contents

1. [At a Glance](#1-at-a-glance)
2. [Quick Start](#2-quick-start)
3. [Topics Covered](#3-topics-covered)
4. [Repository Structure](#4-repository-structure)
5. [API Reference](#5-api-reference)
6. [Concept Deep-Dives](#6-concept-deep-dives)
7. [Complexity & Numerical Behaviour](#7-complexity--numerical-behaviour)
8. [How Correctness Is Verified](#8-how-correctness-is-verified)
9. [Design Philosophy](#9-design-philosophy)
10. [Known Limitations](#10-known-limitations)
11. [Roadmap](#11-roadmap)
12. [FAQ / Troubleshooting](#12-faq--troubleshooting)
13. [Learning Source](#13-learning-source)
14. [Contributing](#14-contributing)
15. [License](#15-license)

---

## 1. At a Glance

| | |
|---|---|
| **Language** | Python 3.10+ |
| **Runtime dependencies** | None (standard library only) |
| **Test / demo dependencies** | `numpy`, `scipy` (`explorations/` only), `pytest` |
| **Matrix format** | Plain list of lists, e.g. `[[1, 2], [3, 4]]` (NumPy arrays are accepted and converted) |
| **Error style** | Fail loudly: `ValueError` with a specific message, never a silently wrong number |
| **Tests** | 134, run on Python 3.10 / 3.11 / 3.12 in CI |

**Why this repo exists.** Strang's course repeats one idea in every lecture: *matrices act on vectors*. It is easy to lose that intuition behind a single line like `A @ B` or `np.linalg.inv(A)`. Implementing row reduction, cofactor expansion and eigenvalue methods by hand makes the mechanics concrete: multiplication is a combination of columns, determinants measure volume scaling, elimination simplifies a transformation, and eigenvectors are the directions a matrix only stretches.

---

## 2. Quick Start

### Install

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
pip install -r requirements-dev.txt     # numpy, scipy, pytest
```

The algorithms themselves need only the standard library; the install above is for verification, tests and `explorations/`.

### Run a worked example

Each module has a `__main__` block that prints its steps and cross-checks NumPy. Run them **from the repo root** with `-m` (the modules share `utils.py`, so running the file path directly won't work):

```bash
python -m matrix_operations.addition_subtraction
python -m matrix_operations.multiplication
python -m matrix_operations.determinant
python -m matrix_operations.matrix_inverse
python -m matrix_operations.gaussian_elimination
python -m matrix_operations.eigen
```

### Use it as a library

```python
from matrix_operations.multiplication import matrix_multiply
from matrix_operations.determinant import determinant, determinant_elimination
from matrix_operations.gaussian_elimination import solve
from matrix_operations.matrix_inverse import inverse
from matrix_operations.eigen import eigen, power_iteration

A = [[2, 1], [1, 3]]

matrix_multiply(A, A)               # [[5, 5], [5, 10]]
determinant(A)                      # 5
solve(A, [1, 2])                    # [0.2, 0.6]
inverse(A)                          # [[0.6, -0.2], [-0.2, 0.4]]
eigen(A)                            # ([1.382, 3.618], [[...], [...]])
power_iteration(A)                  # (3.618, [...])  dominant eigenpair
```

### Run the tests

```bash
python -m pytest            # all 134
python -m pytest -k eigen   # just one module
```

---

## 3. Topics Covered

| # | Topic | Strang Lecture | Module | Status |
|---|-------|----------------|--------|:------:|
| 1 | Matrix addition & subtraction | Lecture 1 | `addition_subtraction.py` | ✅ |
| 2 | Matrix multiplication (dot-product, row-picture, column-picture) | Lectures 1–3 | `multiplication.py` | ✅ |
| 3 | Determinants (cofactor expansion **and** O(n³) elimination) | Lectures 18–19 | `determinant.py` | ✅ |
| 4 | Inverse matrices (Gauss-Jordan) | Lecture 3 | `matrix_inverse.py` | ✅ |
| 5 | Gaussian elimination (row echelon + back-substitution) | Lecture 2 | `gaussian_elimination.py` | ✅ |
| 6 | Eigenvalues & eigenvectors (characteristic polynomial, eigenspaces, power iteration) | Lectures 21–22 | `eigen.py` | ✅ |

How the modules depend on each other:

```
utils.py  ◄── every module (validation, tolerances, printing)
determinant.py  ◄── eigen.py (builds the characteristic polynomial)
multiplication.py  ◄── matrix_inverse.py demo only (to show A·A⁻¹ = I)
```

---

## 4. Repository Structure

```
linear-algebra-playground/
│
├── matrix_operations/              # from-scratch library (pure Python)
│   ├── __init__.py
│   ├── utils.py                    # validation, tolerances, mat-vec, printing
│   ├── addition_subtraction.py     # matrix_add, matrix_subtract
│   ├── multiplication.py           # dot-product, column-picture, row-picture
│   ├── determinant.py              # cofactor expansion + elimination
│   ├── gaussian_elimination.py     # solve Ax = b
│   ├── matrix_inverse.py           # Gauss-Jordan inverse
│   └── eigen.py                    # char. polynomial, eigenspaces, power iteration
│
├── explorations/                   # NumPy / SciPy experiments (not from-scratch)
│   ├── README.md                   # what each script explores
│   ├── vectors.py                  matrices.py
│   ├── linear_system.py            column_space_and_singularity.py
│   ├── elimination_and_matrix_factorization.py   lu_decomposition.py
│   ├── inverse_properties.py       ldl_and_conditioning.py
│   └── solver_benchmark.py
│
├── tests/                          # pytest suite (one file per module)
│   ├── conftest.py                 # seeded RNG + random-matrix helper
│   ├── test_addition_subtraction.py   test_multiplication.py
│   ├── test_determinant.py            test_gaussian_elimination.py
│   ├── test_matrix_inverse.py         test_eigen.py
│   └── test_explorations_smoke.py  # every exploration script must still run
│
├── .github/workflows/ci.yml        # pytest on Python 3.10 – 3.12
├── pyproject.toml                  # pytest configuration
├── requirements.txt                # numpy, scipy
├── requirements-dev.txt            # + pytest
├── license.md
└── README.md
```

> **`matrix_operations/` vs `explorations/`:** the first is the from-scratch library; the second is a scratchpad that *deliberately* uses `numpy.linalg` / `scipy.linalg` to see an idea before or after implementing it by hand.

---

## 5. API Reference

All public functions take matrices as lists of lists (or NumPy arrays), never modify their inputs, and return plain Python lists/floats.

### `utils.py`

| Function | Purpose |
|----------|---------|
| `as_matrix(M, name="Matrix")` | Validate and return a copy. Rejects empty, ragged, non-numeric and NaN/inf input. |
| `as_vector(v, name="Vector")` | Same, for 1-D input. |
| `as_square_matrix(M, operation, name)` | `as_matrix` plus a rows == cols check. |
| `shape(M)` | `(rows, cols)` of a validated matrix. |
| `identity(n)` | `n × n` identity as floats. |
| `pivot_tolerance(M, tol=None)` | Threshold below which a pivot counts as zero: `n · ε · max|aᵢⱼ|`, or `tol` if given. |
| `mat_vec(A, v)`, `norm(v)`, `max_abs(M)` | Small numeric helpers. |
| `print_matrix(M, name=None, precision=4)` | Readable one-row-per-line output. |

### `addition_subtraction.py`

| Function | Returns | Raises `ValueError` when |
|----------|---------|--------------------------|
| `matrix_add(A, B)` | `A + B` | shapes differ, or either input is invalid |
| `matrix_subtract(A, B)` | `A − B` | same |

### `multiplication.py`

Three views of the same product — all return an `m × p` matrix for `A (m × n)` and `B (n × p)`:

| Function | View |
|----------|------|
| `matrix_multiply(A, B)` | entry `(i, j)` = row *i* of A · column *j* of B |
| `matrix_multiply_columns(A, B)` | column *j* of AB = combination of A's **columns**, weighted by column *j* of B |
| `matrix_multiply_rows(A, B)` | row *i* of AB = combination of B's **rows**, weighted by row *i* of A |

Raises `ValueError` if the inner dimensions don't match (e.g. `2×3 @ 2×3`).

### `determinant.py`

| Function | Method | Cost |
|----------|--------|------|
| `determinant(M)` | Cofactor expansion along row 0; exact for integers | O(n!) |
| `determinant_elimination(M, tol=None)` | Forward elimination with partial pivoting; product of pivots × (−1)^swaps; returns `0.0` if singular | O(n³) |
| `get_minor(M, i, j)` | `M` with row *i* and column *j* removed | — |

Both raise `ValueError` for non-square, ragged or empty input.

### `gaussian_elimination.py`

| Function | Purpose |
|----------|---------|
| `solve(A, b, tol=None)` | Solve `Ax = b` for square, non-singular `A`. Returns `x` as a list. |
| `forward_elimination(A, b, tol=None)` | Reduce `[A \| b]` to row echelon form (partial pivoting). Returns the augmented matrix. |
| `back_substitution(aug)` | Solve from the bottom row up, given echelon form. |

Raises `ValueError` for non-square `A`, mismatched `b`, or a **singular / numerically singular** system.

### `matrix_inverse.py`

| Function | Purpose |
|----------|---------|
| `inverse(A, tol=None)` | Gauss-Jordan inverse via `[A \| I] → [I \| A⁻¹]` with partial pivoting. Raises `ValueError` if `A` is singular or not square. |

### `eigen.py`

| Function | Purpose |
|----------|---------|
| `characteristic_polynomial(A)` | Coefficients `[1, −tr, …]` (highest power first) for 2×2 and 3×3. `NotImplementedError` beyond 3×3. |
| `eigenvalues(A)` | Real eigenvalues, **ascending, with multiplicity**. `ValueError` if any are complex. |
| `eigenspace(A, lam)` | Unit basis vectors for the eigenspace at `lam` (one per free variable). |
| `eigenvector_for(A, lam)` | First vector of `eigenspace`. |
| `eigen(A)` | `(values, vectors)`; `vectors[i]` is a unit eigenvector for `values[i]`. A repeated eigenvalue appears once per independent eigenvector, so **`len(values) < n` means the matrix is defective**. |
| `power_iteration(A, num_iterations=1000, tol=1e-10, start=None)` | `(λ, v)` for the dominant eigenpair, any square size. Emits a `RuntimeWarning` if it doesn't converge. |

---

## 6. Concept Deep-Dives

### 6.1 Matrix Addition & Subtraction
**File:** `addition_subtraction.py`

Entrywise arithmetic on same-shaped matrices:

```
(A + B)[i][j] = A[i][j] + B[i][j]
(A − B)[i][j] = A[i][j] − B[i][j]
```

**Learning goal:** the baseline for "matrices as objects you can do arithmetic with," before multiplication introduces the interesting row/column structure.

---

### 6.2 Matrix Multiplication
**File:** `multiplication.py`

The same result computed three ways, because each teaches something different:

- **`matrix_multiply`** — the standard definition: entry `(i, j)` of `AB` is the dot product of row `i` of `A` and column `j` of `B`.
- **`matrix_multiply_columns`** — the **column picture**: column `j` of `AB` is a linear combination of the *columns* of `A`, weighted by column `j` of `B`.
- **`matrix_multiply_rows`** — the **row picture**: row `i` of `AB` is a linear combination of the *rows* of `B`, weighted by row `i` of `A`.

All three are mathematically identical; the tests confirm they agree with each other and with `np.matmul` on square and non-square inputs.

**Learning goal:** stop seeing multiplication as "just dot products" and start seeing `AB` as *combinations of A's columns* — the idea that later explains column space, rank, and why `Ax` is a combination of A's columns.

---

### 6.3 Determinants
**File:** `determinant.py`

Two implementations, side by side:

- **`determinant`** — **cofactor expansion** along the first row:

  ```
  det(A) = Σ_j (−1)^j · A[0][j] · det(minor(A, 0, j))
  ```

  with base cases 1×1 (`A[0][0]`) and 2×2 (`ad − bc`). Exact for integer matrices, but `O(n!)`.
- **`determinant_elimination`** — forward elimination with partial pivoting to an upper-triangular `U`; the determinant is the product of the pivots, with a sign flip per row swap. `O(n³)`.

**Learning goal:** connect the determinant to volume scaling and invertibility, and see that the "formula" and "pivots" definitions agree. The tests also check `det(AB) = det(A)·det(B)` and "a row swap flips the sign".

---

### 6.4 Gaussian Elimination
**File:** `gaussian_elimination.py`

Solves `Ax = b` in two stages:

1. **Forward elimination** — reduce `[A | b]` to row echelon form using partial pivoting (swap in the row with the largest entry in the column).
2. **Back-substitution** — solve for `x` from the bottom row upward; each row has one fewer unknown than the row above.

A pivot with magnitude ≤ `n · ε · max|aᵢⱼ|` counts as zero, so **numerically singular** systems (rows parallel up to one rounding error) raise a clear error instead of returning astronomically large garbage.

**Learning goal:** this is the engine behind everything else in the repo.

---

### 6.5 Inverse Matrices
**File:** `matrix_inverse.py`

**Gauss-Jordan elimination:** build `[A | I]`, apply row operations (partial pivoting, scale each pivot to 1, clear the column *above and below*) until the left half is `I`. The right half is then `A⁻¹`.

Singularity is detected from the pivots themselves rather than from `det(A) == 0` — which would be `O(n!)` via cofactors and unreliable in floating point.

**Learning goal:** derive the inverse mechanically. It is the same machinery as `solve`, but solving `n` systems at once (one per column of `I`).

---

### 6.6 Eigenvalues & Eigenvectors
**File:** `eigen.py` (uses `determinant.py`)

Two complementary approaches, mirroring the two halves of Strang's treatment:

**Characteristic polynomial (exact, 2×2 and 3×3).**
- 2×2: roots of `λ² − tr(A)λ + det(A) = 0` via the quadratic formula.
- 3×3: `λ³ − tr(A)λ² + (sum of principal 2×2 minors)λ − det(A) = 0`, derived by hand, solved by a hand-written cubic solver. It uses the discriminant `D = −(4p³ + 27q²)` of the depressed cubic: `D > 0` → three distinct real roots (trigonometric form); `D ≈ 0` → repeated root (closed form); `D < 0` → complex roots, rejected.

**Eigenvectors via eigenspaces.** For each eigenvalue `λ`, solve `(A − λI)v = 0` with reduced row echelon form; one basis vector per free variable. Consequences:

| Matrix | Result |
|--------|--------|
| `[[4,1],[2,3]]` (distinct eigenvalues) | 2 eigenvalues, 2 eigenvectors |
| identity `I₃` (repeated, full eigenspace) | `[1,1,1]` and **three different** eigenvectors |
| `[[2,1],[0,2]]` (repeated, **defective**) | `[2]` and **one** eigenvector → not diagonalizable |

**Power iteration (approximate, any size).** Repeatedly apply `A` and renormalize; the vector converges to the eigenvector of the largest-magnitude eigenvalue, read off with the Rayleigh quotient `(vᵀAv)/(vᵀv)`. Stops when the residual `‖Av − λv‖` is small and warns if it never gets there.

**Learning goal:** see eigenvectors as "directions a matrix doesn't rotate, only scales" — the tests verify `Av ≈ λv` for every pair rather than trusting the numbers.

---

## 7. Complexity & Numerical Behaviour

| Routine | Time | Notes |
|---------|------|-------|
| `matrix_add` / `matrix_subtract` | O(mn) | |
| `matrix_multiply` (all 3 views) | O(mnp) | |
| `determinant` | **O(n!)** | exact for integers; impractical past ~6×6 |
| `determinant_elimination` | O(n³) | floating point; tolerance-aware |
| `solve` | O(n³) | partial pivoting |
| `inverse` | O(n³) | partial pivoting |
| `eigenvalues` | O(1) after the polynomial | 2×2 / 3×3 only |
| `power_iteration` | O(k·n²) | `k` iterations; convergence rate ≈ \|λ₂/λ₁\| |

**Tolerances.** "Is this pivot zero?" is never `== 0`. The default threshold is `n · ε · max|aᵢⱼ|` (ε ≈ 2.2·10⁻¹⁶), the same idea LAPACK and NumPy's `matrix_rank` use. Pass `tol=` to override. This rejects `[[1, 2], [1, 2.0000000000000004]]` as singular, yet still solves the ill-conditioned (but invertible) 6×6 Hilbert system correctly.

---

## 8. How Correctness Is Verified

The `tests/` suite (134 tests, run in CI on Python 3.10–3.12) works at four levels:

1. **Against NumPy** — seeded random matrices of many sizes compared with `np.add`, `np.matmul`, `np.linalg.det`, `inv`, `solve`, `eigvalsh`.
2. **Mathematical properties** — `A·A⁻¹ = I`, `(AB)⁻¹ = B⁻¹A⁻¹`, `det(AB) = det(A)det(B)`, `Av = λv` for every eigenpair, all three multiplication views agree.
3. **Hard cases** — zero pivots that force a row swap, repeated and defective eigenvalues, ill-conditioned Hilbert systems, numerically singular matrices, a 300-matrix triangular fuzz test.
4. **Error paths** — singular, non-square, ragged, empty, non-finite, complex eigenvalues: each must raise the right error.

Plus a **smoke test** that runs every script in `explorations/`, so the demos can't silently rot.

Each module's `if __name__ == "__main__":` block remains the human-readable worked example; the tests are the safety net.

---

## 9. Design Philosophy

- **Manual first, NumPy second.** Library code uses only lists and loops. NumPy lives in tests and demo cross-checks.
- **Fail loudly.** Bad input raises `ValueError` with a specific message. Validation is implemented once, in `utils.py`.
- **Explicit tolerances.** Size-scaled thresholds, overridable with `tol=`.
- **Show the work.** Every `__main__` block prints inputs, the result and the NumPy comparison.
- **Never mutate the caller's data.** Every routine works on a copy.

---

## 10. Known Limitations

- **`determinant()`** is O(n!) — use `determinant_elimination()` for anything larger than ~6×6.
- **Eigenvalues beyond 3×3** are not supported by the characteristic-polynomial method (`NotImplementedError`); `power_iteration` finds only the dominant pair.
- **Complex eigenvalues** are not supported (e.g. rotation matrices) — a `ValueError` is raised.
- **Near-repeated roots:** the cubic solver treats roots closer than about 10⁻⁶ (relative) as repeated, so nearly-defective matrices can lose a few digits.
- **Equal-magnitude dominant eigenvalues** (e.g. +1 and −1) stop `power_iteration` from converging; it warns rather than answering wrongly.
- **Eigenspace bases are not orthogonalised** for repeated eigenvalues.
- **Square systems only:** `solve` needs a square, non-singular `A`.

---

## 11. Roadmap

- [x] Shared `utils.py` (validation, tolerances, printing)
- [x] `pytest` suite validating every module against NumPy, plus CI
- [x] Determinant via elimination (O(n³)) alongside cofactor expansion
- [x] From-scratch inverse (Gauss-Jordan)
- [ ] From-scratch `lu_decomposition.py` (`PA = LU`) — Strang Lecture 4
- [ ] Reduced row echelon form, rank, and the four fundamental subspaces — Lectures 6–10
- [ ] Matplotlib visualizations: eigenvector directions, determinant as area/volume
- [ ] QR iteration for general eigenvalues (beyond 3×3, and complex)
- [ ] SVD and least squares (Strang Ch. 7–8) — stretch goal

---

## 12. FAQ / Troubleshooting

**`ImportError: attempted relative import with no known parent package`**
You ran a file path directly. Run from the repo root as a module: `python -m matrix_operations.eigen`.

**`ModuleNotFoundError: No module named 'matrix_operations'`**
You're not in the repo root. `cd` into the folder that contains `matrix_operations/` first.

**`ModuleNotFoundError: No module named 'numpy'` / `'scipy'`**
Only the verification steps and `explorations/` need them: `pip install -r requirements-dev.txt`.

**`ValueError: Matrix is singular`**
`solve` / `inverse` found no usable pivot. The matrix has dependent rows, or is so close to it that floating point can't tell. Pass a smaller `tol=` only if you're sure it's merely ill-conditioned.

**`ValueError: Matrix has complex eigenvalues`**
The matrix has no real eigenvalues (e.g. a pure rotation). Only the real case is implemented.

**`eigen()` returned fewer than *n* pairs.**
That's intentional — the matrix is defective (see [6.6](#66-eigenvalues--eigenvectors)).

**`RuntimeWarning: power_iteration did not converge`**
The two largest-magnitude eigenvalues are (nearly) equal, or you need more `num_iterations`.

---

## 13. Learning Source

**Gilbert Strang — *Introduction to Linear Algebra*** (6th Edition), the companion to MIT OpenCourseWare **18.06 Linear Algebra**.

---

## 14. Contributing

This is primarily a personal learning log, but if you're working through the same material and spot a bug, an unhandled edge case, or a cleaner way to derive something by hand, open an issue or a PR. Please run `python -m pytest` first and add a test for anything you fix.

---

## 15. License

MIT License — free to use, modify, and learn from. See [`license.md`](license.md).
