# Linear Algebra Playground

![Python](https://img.shields.io/badge/python-3.x-blue)
![Status](https://img.shields.io/badge/status-core%20topics%20complete-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A from-scratch implementation of core linear algebra algorithms in pure Python, built while working through **Gilbert Strang's *Introduction to Linear Algebra*** (MIT 18.06). No `numpy.linalg` shortcuts for the algorithms themselves — every method is coded by hand first, then cross-checked against NumPy for correctness. NumPy appears only as a verification tool (and, in one narrow case, as a general-purpose polynomial root-finder — see [Eigenvalues & Eigenvectors](#7-eigenvalues--eigenvectors)).

If you're also working through 18.06 or Strang's textbook, this repo doubles as a study log: each script is runnable on its own, prints its work step by step, and states which lecture the concept comes from.

---

## Table of Contents

- [Why This Repo Exists](#why-this-repo-exists)
- [Topics Covered](#topics-covered)
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

It's easy to lose that intuition behind a single line like `A @ B` or `np.linalg.inv(A)`. This repo exists to slow that down — implementing row reduction, cofactor expansion, and iterative eigenvalue methods by hand so the mechanics are actually understood, not just imported.

---

## Topics Covered

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

---

## Repository Structure

```
linear-algebra-playground/
│
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

---

## Getting Started

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
```

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

Computed via **cofactor expansion** along the first row:

```
det(A) = Σ_j (-1)^j · A[0][j] · det(minor(A, 0, j))
```

with base cases for 1×1 (`det = A[0][0]`) and 2×2 (`det = ad - bc`).

**Complexity note:** cofactor expansion is `O(n!)` — fine for the small matrices used here (up to 4×4 in the test block), but it does not scale. Gaussian elimination (see below) offers an `O(n³)` alternative for computing determinants, which is one of the connections worth exploring in the Roadmap.

**Learning goal:** connect the determinant to volume scaling and invertibility — a matrix is invertible exactly when `det(A) ≠ 0`, which is exactly the check `inverse_matrix.py` uses before attempting to invert.

---

### 4. Inverse Matrices
**File:** `inverse_matrix.py` (depends on `determinant.py`)

Computed via **Gauss-Jordan elimination**: build the augmented matrix `[A | I]`, then use row operations (with partial pivoting for numerical stability) to reduce the left half to the identity. Whatever happens to the right half is `A⁻¹`.

Before attempting inversion, the function checks `determinant(A) == 0` and raises a clear error for singular matrices rather than dividing by (near) zero.

**Learning goal:** derive the inverse mechanically via row operations rather than a formula — this is the same elimination machinery used in `gaussian_elimination.py`, just applied to the identity matrix instead of a single vector `b`.

---

### 5. Gaussian Elimination
**File:** `gaussian_elimination.py`

Solves `Ax = b` in two stages:

1. **Forward elimination** — reduce the augmented matrix `[A | b]` to row echelon form using partial pivoting.
2. **Back-substitution** — solve for `x` from the bottom row upward, since each row now has one fewer unknown than the row above it.

Raises a clear error if elimination hits a zero pivot with no valid row to swap in (a singular system).

**Learning goal:** this is the general-purpose engine behind `inverse_matrix.py` — instead of solving one system `Ax = b`, Gauss-Jordan solves `n` systems at once (one per column of the identity matrix).

---

### 6. Eigenvalues & Eigenvectors
**File:** `eigen.py` (depends on `determinant.py`)

Two complementary approaches, matching the two halves of Strang's treatment:

- **Characteristic polynomial** (exact, small matrices only): for a 2×2 matrix, the eigenvalues are the roots of `λ² - trace(A)λ + det(A) = 0`, solved directly with the quadratic formula. For 3×3, the cubic `λ³ - trace(A)λ² + (sum of principal minors)λ - det(A) = 0` is derived by hand from the same identities, and its roots are found with `numpy.roots` — used strictly as a generic polynomial root-finder on coefficients that were already derived manually, not as a linear-algebra eigenvalue solver. Beyond 3×3 this approach isn't implemented (see [Known Limitations](#known-limitations)).
- **Power iteration** (approximate, any size): repeatedly apply `A` to a vector and renormalize; the vector converges toward the eigenvector of the largest-magnitude eigenvalue, and the corresponding eigenvalue is read off with the Rayleigh quotient `(vᵀAv) / (vᵀv)`.

Once an eigenvalue `λ` is known, its eigenvector is found by solving the homogeneous system `(A - λI)v = 0` for a non-trivial solution — implemented as a small null-space finder built on the same row-reduction idea as `gaussian_elimination.py`.

**Learning goal:** see eigenvectors as "directions a matrix doesn't rotate, only scales" — verified directly in the test block by checking `Av ≈ λv` for every computed pair, rather than just trusting the numbers.

---

## How Correctness Is Verified

Every script follows the same pattern:

1. Run the from-scratch implementation on one or more example matrices.
2. Print the intermediate steps and final result.
3. Cross-check the result against the equivalent NumPy call (`np.add`, `np.matmul`, `np.linalg.det`, `np.linalg.inv`, `np.linalg.solve`, `np.linalg.eig`).
4. Deliberately trigger error cases (singular matrices, non-square input, ragged rows, complex eigenvalues) to confirm they fail loudly and clearly instead of silently returning wrong numbers.

This is intentionally simple (no formal test framework yet — see [Roadmap](#roadmap)) but catches the failure modes that matter most while learning: sign errors in cofactor expansion, off-by-one indexing in back-substitution, and pivoting bugs in elimination.

---

## Design Philosophy

- **Manual first, NumPy second.** Every algorithm is implemented with plain Python lists and loops before anything is checked against NumPy.
- **Fail loudly.** Empty matrices, ragged rows, dimension mismatches, singular matrices, and complex eigenvalues all raise a `ValueError` with a specific message rather than producing silently wrong output.
- **Show the work.** Every script's `if __name__ == "__main__":` block prints inputs, the computed result, and (where applicable) the NumPy comparison — treat these as worked examples, not just smoke tests.
- **One narrow, documented exception to "no numpy.linalg":** `eigen.py` uses `numpy.roots` to solve the 3×3 characteristic polynomial's cubic. This is a generic polynomial root-finder, not an eigenvalue routine — the polynomial's coefficients are still derived by hand from `trace`, `determinant`, and the principal minors.

---

## Known Limitations

Worth knowing before relying on this code for anything beyond learning:

- **`determinant.py`** is `O(n!)` (cofactor expansion) — impractical much past 5×5 or 6×6.
- **`eigen.py`'s characteristic-polynomial method only supports 2×2 and 3×3 matrices** — larger matrices raise `NotImplementedError` and should use `power_iteration` instead, which only recovers the *dominant* (largest-magnitude) eigenvalue/eigenvector, not the full spectrum.
- **Complex eigenvalues are not supported.** Both `eigenvalues()` and `power_iteration()` assume real eigenvalues and raise a `ValueError` otherwise (e.g. rotation matrices).
- **No tolerance-aware equality anywhere** except where explicitly noted (e.g. `power_iteration`'s convergence check) — floating-point results are compared with `np.allclose` in the verification step, not inside the algorithms themselves.

---

## Roadmap

- [ ] Add a shared `utils/` module (validation, printing helpers) to reduce duplication across scripts
- [ ] Add a proper `tests/` folder (e.g. `pytest`) validating manual implementations against NumPy, replacing the current inline test blocks
- [ ] Add visualizations for each transformation (2D/3D) using Matplotlib — especially eigenvector directions and determinant-as-area/volume
- [ ] Extend `eigen.py`'s characteristic-polynomial method beyond 3×3, or generalize to complex eigenvalues
- [ ] Compute determinants via Gaussian elimination (`O(n³)`) as a faster alternative to cofactor expansion, and compare the two
- [ ] Extend to SVD and least-squares (Strang Ch. 7–8) as a stretch goal

---

## Learning Source

**Gilbert Strang — *Introduction to Linear Algebra*** (6th Edition)
Companion to MIT OpenCourseWare **18.06 Linear Algebra**

---

## Contributing

This is primarily a personal learning log, but if you're working through the same material and spot a bug, an edge case that isn't handled, or a cleaner way to derive something by hand, feel free to open an issue or a PR.

---

## License

MIT License — free to use, modify, and learn from.
