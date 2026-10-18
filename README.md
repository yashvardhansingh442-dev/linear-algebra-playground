# Linear Algebra Playground

<<<<<<< HEAD
[![CI](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml/badge.svg)](https://github.com/yashvardhansingh442-dev/linear-algebra-playground/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-core%20topics%20complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A from-scratch implementation of core linear algebra algorithms in pure Python, built while working through **Gilbert Strang's *Introduction to Linear Algebra*** (MIT 18.06). No `numpy.linalg` shortcuts for the algorithms themselves — every method in [`matrix_operations/`](matrix_operations) is coded by hand with plain lists and loops, then cross-checked against NumPy in a `pytest` suite. NumPy is a verification tool only; the library code itself does not import it.

If you're also working through 18.06 or Strang's textbook, this repo doubles as a study log: each module is runnable on its own, prints its work step by step, and states which lecture the concept comes from. The [`explorations/`](explorations) folder holds the companion NumPy/SciPy experiments (LU, conditioning, sparse solvers, …).
=======
![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-core%20topics%20complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A from-scratch implementation of core linear algebra algorithms in pure Python, built while working through **Gilbert Strang's *Introduction to Linear Algebra*** (MIT 18.06). No `numpy.linalg` shortcuts for the algorithms themselves — every method is coded by hand first, then cross-checked against NumPy for correctness. NumPy appears only as a verification tool (and, in one narrow case, as a general-purpose polynomial root-finder — see [Eigenvalues & Eigenvectors](#7-eigenvalues--eigenvectors)).

If you're also working through 18.06 or Strang's textbook, this repo doubles as a study log: each script is runnable on its own, prints its work step by step, and states which lecture the concept comes from.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Table of Contents

- [Why This Repo Exists](#why-this-repo-exists)
- [Topics Covered](#topics-covered)
<<<<<<< HEAD
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Concept Deep-Dives](#concept-deep-dives)
=======
- [Progress Tracker](#progress-tracker)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Concept Deep-Dives](#concept-deep-dives)
  - [1. Matrix Addition & Subtraction](#1-matrix-addition--subtraction)
  - [2. Matrix Multiplication](#2-matrix-multiplication)
  - [3. Determinants](#3-determinants)
  - [4. Inverse Matrices](#4-inverse-matrices)
  - [5. Gaussian Elimination](#5-gaussian-elimination)
  - [6. Eigenvalues & Eigenvectors](#6-eigenvalues--eigenvectors)
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
- [How Correctness Is Verified](#how-correctness-is-verified)
- [Design Philosophy](#design-philosophy)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Learning Source](#learning-source)
- [Contributing](#contributing)
- [License](#license)

---

## Why This Repo Exists

Strang's course is built around one idea repeated in every lecture: **matrices act on vectors**, and almost every algorithm in linear algebra is a different lens on that same fact. Multiplication is a combination of columns. Determinants measure how much a transformation scales volume. Elimination is just a systematic way of simplifying that transformation. Eigenvectors are the special directions a matrix doesn't rotate, only stretches.

<<<<<<< HEAD
It's easy to lose that intuition behind a single line like `A @ B` or `np.linalg.inv(A)`. This repo exists to slow that down — implementing row reduction, cofactor expansion, and eigenvalue methods by hand so the mechanics are actually understood, not just imported.
=======
It's easy to lose that intuition behind a single line like `A @ B` or `np.linalg.inv(A)`. This repo exists to slow that down — implementing row reduction, cofactor expansion, and iterative eigenvalue methods by hand so the mechanics are actually understood, not just imported.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Topics Covered

<<<<<<< HEAD
| # | Topic | Strang Lecture Ref. | Module | Status |
|---|-------|----------------------|--------|--------|
| 1 | Matrix Addition & Subtraction | Lecture 1 | `addition_subtraction.py` | ✅ Done |
| 2 | Matrix Multiplication (dot-product, row-picture, column-picture) | Lecture 1–3 | `multiplication.py` | ✅ Done |
| 3 | Determinants (cofactor expansion **and** O(n³) elimination) | Lecture 18–19 | `determinant.py` | ✅ Done |
| 4 | Inverse Matrices (Gauss-Jordan method) | Lecture 3 | `matrix_inverse.py` | ✅ Done |
| 5 | Gaussian Elimination (row echelon + back-substitution) | Lecture 2 | `gaussian_elimination.py` | ✅ Done |
| 6 | Eigenvalues & Eigenvectors (characteristic polynomial, eigenspaces, power iteration) | Lecture 21–22 | `eigen.py` | ✅ Done |
=======
| # | Topic | Strang Lecture Ref. | File | Status |
|---|-------|----------------------|------|--------|
| 1 | Matrix Addition & Subtraction | Lecture 1 | `addition_subtraction.py` | ✅ Done |
| 2 | Matrix Multiplication (dot-product, row-picture, column-picture) | Lecture 1–3 | `multiplication.py` | ✅ Done |
| 3 | Determinants (cofactor expansion) | Lecture 18–19 | `determinant.py` | ✅ Done |
| 4 | Inverse Matrices (Gauss-Jordan method) | Lecture 3 | `inverse_matrix.py` | ✅ Done |
| 5 | Gaussian Elimination (row echelon + back-substitution) | Lecture 2 | `gaussian_elimination.py` | ✅ Done |
| 6 | Eigenvalues & Eigenvectors (characteristic polynomial, power iteration) | Lecture 21–22 | `eigen.py` | ✅ Done |

---

## Progress Tracker

- [x] Matrix Addition & Subtraction
- [x] Matrix Multiplication
- [x] Determinant
- [x] Inverse
- [x] Gaussian Elimination
- [x] Eigenvalues

**Core topics are complete.** Current focus has shifted to the items in [Roadmap](#roadmap) — a shared `utils/` module, an actual `tests/` suite, visualizations, and the SVD/least-squares stretch goal.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Repository Structure

```
linear-algebra-playground/
│
<<<<<<< HEAD
├── matrix_operations/              # from-scratch implementations (pure Python)
│   ├── utils.py                    # shared validation, tolerances, printing helpers
│   ├── addition_subtraction.py     # matrix_add, matrix_subtract
│   ├── multiplication.py           # dot-product, row-picture, column-picture views
│   ├── determinant.py              # cofactor expansion + elimination-based determinant
│   ├── gaussian_elimination.py     # solves Ax = b via row echelon + back-substitution
│   ├── matrix_inverse.py           # Gauss-Jordan inverse
│   └── eigen.py                    # characteristic polynomial (2x2, 3x3), eigenspaces, power iteration
│
├── explorations/                   # NumPy / SciPy experiments (see explorations/README.md)
│
├── tests/                          # pytest suite: every module checked against NumPy
├── .github/workflows/ci.yml        # runs the tests on Python 3.10 – 3.12
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml                  # pytest configuration
└── README.md
```

**Internal dependencies:** every module imports its validation helpers from `utils.py`, and `eigen.py` also uses `determinant()` from `determinant.py` to build the characteristic polynomial. Keep the files together in `matrix_operations/` if you reorganize.
=======
├── matrix_operations/
│   ├── addition_subtraction.py    # matrix_add, matrix_subtract
│   ├── multiplication.py          # dot-product, row-picture, column-picture views
│   ├── determinant.py             # cofactor expansion
│   ├── inverse_matrix.py          # Gauss-Jordan elimination (imports determinant.py)
│   ├── gaussian_elimination.py    # solves Ax = b via row echelon + back-substitution
│   └── eigen.py                   # characteristic polynomial (2x2, 3x3) + power iteration (imports determinant.py)
│
├── .gitignore
└── README.md
```

> **Planned additions** (see [Roadmap](#roadmap)): a shared `utils/` module for validation/printing helpers, a `tests/` folder with proper unit tests, a `visualizations/` module using Matplotlib, and eventually `svd.py` / `least_squares.py`.

**Note on internal dependencies:** `inverse_matrix.py` and `eigen.py` both import `determinant()` from `determinant.py` to check for singularity. Keep these files together in `matrix_operations/` if you reorganize.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Getting Started

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
```

<<<<<<< HEAD
The algorithms need nothing beyond the standard library. NumPy is used by the verification steps and tests, and SciPy by `explorations/`:

```bash
pip install -r requirements-dev.txt     # numpy, scipy, pytest
```

Run any module as a script to see a step-by-step worked example with a NumPy cross-check (use `-m` from the repo root, since the modules share `utils.py`):

```bash
python -m matrix_operations.addition_subtraction
python -m matrix_operations.multiplication
python -m matrix_operations.determinant
python -m matrix_operations.matrix_inverse
python -m matrix_operations.gaussian_elimination
python -m matrix_operations.eigen
```

Or use them as a library:

```python
from matrix_operations.gaussian_elimination import solve
from matrix_operations.matrix_inverse import inverse
from matrix_operations.eigen import eigen

solve([[2, 1], [1, 3]], [1, 2])      # [0.2, 0.6]
inverse([[2, 1], [1, 1]])            # [[1.0, -1.0], [-1.0, 2.0]]
eigen([[4, 1], [2, 3]])              # ([2.0, 5.0], [[...], [...]])
```

Run the tests:

```bash
python -m pytest
=======
No dependencies are required to run the core algorithms — they're pure Python. NumPy is used only for the optional verification step at the bottom of each script (and internally by `eigen.py`'s cubic-root solver), so install it if you want that check to run:

```bash
pip install numpy
```

Each script is runnable standalone and prints a step-by-step breakdown of the computation, not just the final result — matching how Strang works through problems in lecture:

```bash
python matrix_operations/addition_subtraction.py
python matrix_operations/multiplication.py
python matrix_operations/determinant.py
python matrix_operations/inverse_matrix.py
python matrix_operations/gaussian_elimination.py
python matrix_operations/eigen.py
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
```

---

## Concept Deep-Dives

### 1. Matrix Addition & Subtraction
**File:** `addition_subtraction.py`

The simplest operations, but the starting point for everything else: entrywise addition/subtraction of two same-shaped matrices.

```
(A + B)[i][j] = A[i][j] + B[i][j]
(A - B)[i][j] = A[i][j] - B[i][j]
```

**Learning goal:** treat this as the baseline for "matrices as objects you can do arithmetic with," before multiplication introduces the more interesting row/column structure.

---

### 2. Matrix Multiplication
**File:** `multiplication.py`

Implements the same result three different ways, because each way teaches something different:

- **`matrix_multiply`** — the standard definition: entry `(i, j)` of `AB` is the dot product of row `i` of `A` and column `j` of `B`.
- **`matrix_multiply_columns`** — the **column picture**: column `j` of `AB` is a linear combination of the *columns* of `A`, weighted by column `j` of `B`.
- **`matrix_multiply_rows`** — the **row picture**: row `i` of `AB` is a linear combination of the *rows* of `B`, weighted by row `i` of `A`.

All three are mathematically identical — the test block confirms they agree with each other and with `np.matmul` on both square and non-square examples.

**Learning goal:** stop seeing multiplication as "just dot products" and start seeing `AB` as *combinations of A's columns* — the same idea that later explains column space, rank, and why `Ax` is a combination of A's columns for a single vector `x`.

---

### 3. Determinants
**File:** `determinant.py`

<<<<<<< HEAD
Two implementations, side by side:

- **`determinant`** — **cofactor expansion** along the first row:

  ```
  det(A) = Σ_j (-1)^j · A[0][j] · det(minor(A, 0, j))
  ```

  with base cases for 1×1 (`det = A[0][0]`) and 2×2 (`det = ad - bc`). Exact for integer matrices, but `O(n!)`.
- **`determinant_elimination`** — forward elimination with partial pivoting to an upper-triangular `U`; the determinant is the product of the pivots, with a sign flip per row swap. `O(n³)`, and it returns `0.0` when no usable pivot exists (singular).

**Learning goal:** connect the determinant to volume scaling and invertibility — and see that the "formula" definition and the "pivots" definition agree. The tests check both against `np.linalg.det`, plus properties like `det(AB) = det(A)·det(B)` and "a row swap flips the sign".
=======
Computed via **cofactor expansion** along the first row:

```
det(A) = Σ_j (-1)^j · A[0][j] · det(minor(A, 0, j))
```

with base cases for 1×1 (`det = A[0][0]`) and 2×2 (`det = ad - bc`).

**Complexity note:** cofactor expansion is `O(n!)` — fine for the small matrices used here (up to 4×4 in the test block), but it does not scale. Gaussian elimination (see below) offers an `O(n³)` alternative for computing determinants, which is one of the connections worth exploring in the Roadmap.

**Learning goal:** connect the determinant to volume scaling and invertibility — a matrix is invertible exactly when `det(A) ≠ 0`, which is exactly the check `inverse_matrix.py` uses before attempting to invert.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

### 4. Inverse Matrices
<<<<<<< HEAD
**File:** `matrix_inverse.py`

Computed via **Gauss-Jordan elimination**: build the augmented matrix `[A | I]`, then use row operations (with partial pivoting for numerical stability) to reduce the left half to the identity. Whatever happens to the right half is `A⁻¹`.

Singularity is detected from the pivots themselves: if a column has no pivot larger than `n · ε · max|aᵢⱼ|`, a `ValueError` is raised. This is more robust than testing `det(A) == 0` (which is `O(n!)` via cofactors and unreliable in floating point).
=======
**File:** `inverse_matrix.py` (depends on `determinant.py`)

Computed via **Gauss-Jordan elimination**: build the augmented matrix `[A | I]`, then use row operations (with partial pivoting for numerical stability) to reduce the left half to the identity. Whatever happens to the right half is `A⁻¹`.

Before attempting inversion, the function checks `determinant(A) == 0` and raises a clear error for singular matrices rather than dividing by (near) zero.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

**Learning goal:** derive the inverse mechanically via row operations rather than a formula — this is the same elimination machinery used in `gaussian_elimination.py`, just applied to the identity matrix instead of a single vector `b`.

---

### 5. Gaussian Elimination
**File:** `gaussian_elimination.py`

Solves `Ax = b` in two stages:

1. **Forward elimination** — reduce the augmented matrix `[A | b]` to row echelon form using partial pivoting.
2. **Back-substitution** — solve for `x` from the bottom row upward, since each row now has one fewer unknown than the row above it.

<<<<<<< HEAD
Raises a clear error if elimination finds no usable pivot (a singular system). "Usable" is judged with a size-scaled tolerance, so *numerically* singular systems (e.g. rows that are parallel up to one rounding error) are rejected instead of returning astronomically large garbage.

**Learning goal:** this is the general-purpose engine behind `matrix_inverse.py` — instead of solving one system `Ax = b`, Gauss-Jordan solves `n` systems at once (one per column of the identity matrix).
=======
Raises a clear error if elimination hits a zero pivot with no valid row to swap in (a singular system).

**Learning goal:** this is the general-purpose engine behind `inverse_matrix.py` — instead of solving one system `Ax = b`, Gauss-Jordan solves `n` systems at once (one per column of the identity matrix).
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

### 6. Eigenvalues & Eigenvectors
**File:** `eigen.py` (depends on `determinant.py`)

Two complementary approaches, matching the two halves of Strang's treatment:

<<<<<<< HEAD
- **Characteristic polynomial** (exact, small matrices only): for a 2×2 matrix, the eigenvalues are the roots of `λ² - trace(A)λ + det(A) = 0`, solved with the quadratic formula. For 3×3, the cubic `λ³ - trace(A)λ² + (sum of principal minors)λ - det(A) = 0` is derived by hand from the same identities and solved with a hand-written cubic solver (discriminant test → trigonometric form for three distinct roots, closed form for repeated roots). Beyond 3×3 this approach isn't implemented (see [Known Limitations](#known-limitations)).
- **Power iteration** (approximate, any size): repeatedly apply `A` to a vector and renormalize; the vector converges toward the eigenvector of the largest-magnitude eigenvalue, and the corresponding eigenvalue is read off with the Rayleigh quotient `(vᵀAv) / (vᵀv)`. It stops when the residual `‖Av − λv‖` is small, and warns if it can't get there.

Once an eigenvalue `λ` is known, its **eigenspace** is found by solving `(A - λI)v = 0` — a null-space basis built from reduced row echelon form, one vector per free variable. So a repeated eigenvalue returns as many independent eigenvectors as it really has: the identity matrix gets a full basis, while a defective matrix like `[[2, 1], [0, 2]]` gets only one — `eigen()` returns fewer than `n` pairs, which is exactly the signal that the matrix isn't diagonalizable.

**Learning goal:** see eigenvectors as "directions a matrix doesn't rotate, only scales" — verified directly in the tests by checking `Av ≈ λv` for every computed pair, rather than just trusting the numbers.
=======
- **Characteristic polynomial** (exact, small matrices only): for a 2×2 matrix, the eigenvalues are the roots of `λ² - trace(A)λ + det(A) = 0`, solved directly with the quadratic formula. For 3×3, the cubic `λ³ - trace(A)λ² + (sum of principal minors)λ - det(A) = 0` is derived by hand from the same identities, and its roots are found with `numpy.roots` — used strictly as a generic polynomial root-finder on coefficients that were already derived manually, not as a linear-algebra eigenvalue solver. Beyond 3×3 this approach isn't implemented (see [Known Limitations](#known-limitations)).
- **Power iteration** (approximate, any size): repeatedly apply `A` to a vector and renormalize; the vector converges toward the eigenvector of the largest-magnitude eigenvalue, and the corresponding eigenvalue is read off with the Rayleigh quotient `(vᵀAv) / (vᵀv)`.

Once an eigenvalue `λ` is known, its eigenvector is found by solving the homogeneous system `(A - λI)v = 0` for a non-trivial solution — implemented as a small null-space finder built on the same row-reduction idea as `gaussian_elimination.py`.

**Learning goal:** see eigenvectors as "directions a matrix doesn't rotate, only scales" — verified directly in the test block by checking `Av ≈ λv` for every computed pair, rather than just trusting the numbers.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## How Correctness Is Verified

<<<<<<< HEAD
The `tests/` folder holds a `pytest` suite (run it with `python -m pytest`; CI runs it on Python 3.10–3.12). For every module it:

1. Compares the from-scratch result against the equivalent NumPy call (`np.add`, `np.matmul`, `np.linalg.det`, `np.linalg.inv`, `np.linalg.solve`, `np.linalg.eigvalsh`) on seeded random matrices of many sizes.
2. Checks mathematical *properties*, not just values: `A·A⁻¹ = I`, `(AB)⁻¹ = B⁻¹A⁻¹`, `det(AB) = det(A)det(B)`, `Av = λv` for every eigenpair, all three multiplication views agreeing.
3. Covers the tricky inputs: row swaps forced by a zero pivot, repeated and defective eigenvalues, ill-conditioned (Hilbert) systems, numerically singular matrices.
4. Triggers every error path (singular, non-square, ragged, empty, non-finite, complex eigenvalues) and asserts it fails loudly.
5. Smoke-tests every script in `explorations/` so the demos can't silently rot.

Each module's `if __name__ == "__main__":` block is still a human-readable worked example — treat those as the "show the work" layer, and the tests as the safety net.
=======
Every script follows the same pattern:

1. Run the from-scratch implementation on one or more example matrices.
2. Print the intermediate steps and final result.
3. Cross-check the result against the equivalent NumPy call (`np.add`, `np.matmul`, `np.linalg.det`, `np.linalg.inv`, `np.linalg.solve`, `np.linalg.eig`).
4. Deliberately trigger error cases (singular matrices, non-square input, ragged rows, complex eigenvalues) to confirm they fail loudly and clearly instead of silently returning wrong numbers.

This is intentionally simple (no formal test framework yet — see [Roadmap](#roadmap)) but catches the failure modes that matter most while learning: sign errors in cofactor expansion, off-by-one indexing in back-substitution, and pivoting bugs in elimination.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Design Philosophy

<<<<<<< HEAD
- **Manual first, NumPy second.** Every algorithm is implemented with plain Python lists and loops; NumPy appears only in tests and demo cross-checks.
- **Fail loudly.** Empty matrices, ragged rows, dimension mismatches, non-finite entries, singular matrices, and complex eigenvalues all raise a `ValueError` with a specific message rather than producing silently wrong output. Validation lives in one place, `utils.py`.
- **Tolerances are explicit.** "Is this pivot zero?" is answered with a size-scaled threshold (`n · ε · max|aᵢⱼ|`) that can be overridden via `tol=`, never with a bare `== 0`.
- **Show the work.** Every module's `__main__` block prints inputs, the computed result, and the NumPy comparison.
- **Don't mutate the caller's data.** Every routine works on a copy.
=======
- **Manual first, NumPy second.** Every algorithm is implemented with plain Python lists and loops before anything is checked against NumPy.
- **Fail loudly.** Empty matrices, ragged rows, dimension mismatches, singular matrices, and complex eigenvalues all raise a `ValueError` with a specific message rather than producing silently wrong output.
- **Show the work.** Every script's `if __name__ == "__main__":` block prints inputs, the computed result, and (where applicable) the NumPy comparison — treat these as worked examples, not just smoke tests.
- **One narrow, documented exception to "no numpy.linalg":** `eigen.py` uses `numpy.roots` to solve the 3×3 characteristic polynomial's cubic. This is a generic polynomial root-finder, not an eigenvalue routine — the polynomial's coefficients are still derived by hand from `trace`, `determinant`, and the principal minors.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Known Limitations

Worth knowing before relying on this code for anything beyond learning:

<<<<<<< HEAD
- **`determinant()`** is `O(n!)` (cofactor expansion) — impractical much past 5×5 or 6×6. Use `determinant_elimination()` for anything larger.
- **`eigen.py`'s characteristic-polynomial method only supports 2×2 and 3×3 matrices** — larger matrices raise `NotImplementedError` and should use `power_iteration` instead, which only recovers the *dominant* (largest-magnitude) eigenvalue/eigenvector, not the full spectrum.
- **Complex eigenvalues are not supported.** `eigenvalues()` raises a `ValueError` for them (e.g. rotation matrices).
- **Roots closer than ~1e-6 (relative) are treated as repeated** by the cubic solver, so nearly-defective matrices can lose a few digits of accuracy.
- **`power_iteration` can't separate eigenvalues of equal magnitude** (e.g. +1 and −1); it warns instead of returning a wrong answer silently.
- **Square systems only:** `gaussian_elimination.solve` handles square, non-singular `A`. Rectangular, under- and over-determined systems aren't implemented yet.
=======
- **`determinant.py`** is `O(n!)` (cofactor expansion) — impractical much past 5×5 or 6×6.
- **`eigen.py`'s characteristic-polynomial method only supports 2×2 and 3×3 matrices** — larger matrices raise `NotImplementedError` and should use `power_iteration` instead, which only recovers the *dominant* (largest-magnitude) eigenvalue/eigenvector, not the full spectrum.
- **Complex eigenvalues are not supported.** Both `eigenvalues()` and `power_iteration()` assume real eigenvalues and raise a `ValueError` otherwise (e.g. rotation matrices).
- **No tolerance-aware equality anywhere** except where explicitly noted (e.g. `power_iteration`'s convergence check) — floating-point results are compared with `np.allclose` in the verification step, not inside the algorithms themselves.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## Roadmap

<<<<<<< HEAD
- [x] Shared `utils.py` module (validation, tolerances, printing helpers) to remove duplication across scripts
- [x] Proper `tests/` folder (`pytest`) validating manual implementations against NumPy, plus CI
- [x] Compute determinants via elimination (`O(n³)`) as a faster alternative to cofactor expansion
- [ ] From-scratch `lu_decomposition.py` (`PA = LU`) to replace the SciPy demo in `explorations/` — Strang Lecture 4
- [ ] Row-reduced echelon form, rank, and the four fundamental subspaces (Strang Lectures 6–10)
- [ ] Visualizations for each transformation (2D/3D) using Matplotlib — especially eigenvector directions and determinant-as-area/volume
- [ ] General eigenvalue algorithm (QR iteration) to go beyond 3×3 and handle complex eigenvalues
=======
- [ ] Add a shared `utils/` module (validation, printing helpers) to reduce duplication across scripts
- [ ] Add a proper `tests/` folder (e.g. `pytest`) validating manual implementations against NumPy, replacing the current inline test blocks
- [ ] Add visualizations for each transformation (2D/3D) using Matplotlib — especially eigenvector directions and determinant-as-area/volume
- [ ] Extend `eigen.py`'s characteristic-polynomial method beyond 3×3, or generalize to complex eigenvalues
- [ ] Compute determinants via Gaussian elimination (`O(n³)`) as a faster alternative to cofactor expansion, and compare the two
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681
- [ ] Extend to SVD and least-squares (Strang Ch. 7–8) as a stretch goal

---

## Learning Source

**Gilbert Strang — *Introduction to Linear Algebra*** (6th Edition)
Companion to MIT OpenCourseWare **18.06 Linear Algebra**

---

## Contributing

<<<<<<< HEAD
This is primarily a personal learning log, but if you're working through the same material and spot a bug, an edge case that isn't handled, or a cleaner way to derive something by hand, feel free to open an issue or a PR. Please run `python -m pytest` first.
=======
This is primarily a personal learning log, but if you're working through the same material and spot a bug, an edge case that isn't handled, or a cleaner way to derive something by hand, feel free to open an issue or a PR.
>>>>>>> 6d0f8c38f935ff7cdd49549d30a8d1417530f681

---

## License

MIT License — free to use, modify, and learn from.
