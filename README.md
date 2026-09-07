# Linear Algebra Playground

A hands-on implementation of core linear algebra concepts in Python, built while studying **Gilbert Strang's *Introduction to Linear Algebra*** (MIT 18.06). Each topic is coded from scratch (no `numpy.linalg` shortcuts, unless used for verification) to build real intuition for the math, then cross-checked against NumPy for correctness.

---

## 📌 Why This Repo Exists

Strang's course builds linear algebra around **four fundamental subspaces** and the idea that "matrices act on vectors." This repo mirrors that structure: instead of just calling library functions, every algorithm here is implemented manually first, so the underlying mechanics (row reduction, cofactor expansion, iterative eigenvalue methods) are actually understood — not just imported.

---

## 🧩 Topics Covered

| # | Topic | Strang Lecture Ref. | Status |
|---|-------|----------------------|--------|
| 1 | Matrix Addition | Lecture 1 | ✅ Done |
| 2 | Matrix Subtraction | Lecture 1 | ✅ Done |
| 3 | Matrix Multiplication (dot-product, row-picture, column-picture) | Lecture 1–3 | ✅ Done |
| 4 | Determinants (cofactor expansion) | Lecture 18–19 | ✅ Done |
| 5 | Inverse Matrices (Gauss-Jordan method) | Lecture 3 | ✅ Done |
| 6 | Gaussian Elimination (row echelon + back-substitution) | Lecture 2 | ✅ Done |
| 7 | Eigenvalues & Eigenvectors (characteristic polynomial, power iteration) | Lecture 21–22 | ✅ Done |

---

## ✅ Progress Tracker

- [x] Matrix Addition
- [x] Matrix Subtraction
- [x] Matrix Multiplication
- [x] Determinant
- [x] Inverse
- [x] Gaussian Elimination
- [x] Eigenvalues

**Current focus:** Core topics complete — see Roadmap below for what's next (visualizations, tests, SVD/least-squares)

---

## 📂 Repository Structure

```
linear-algebra-playground/
│
├── matrix_operations/
│   ├── addition_subtraction.py    # matrix_add, matrix_subtract
│   ├── multiplication.py          # dot-product, row-picture, column-picture views
│   ├── determinant.py             # cofactor expansion
│   ├── inverse_matrix.py          # Gauss-Jordan elimination
│   ├── gaussian_elimination.py    # solves Ax = b via row echelon + back-substitution
│   └── eigen.py                   # characteristic polynomial (2x2, 3x3) + power iteration
│
├── .gitignore
└── README.md
```

> Planned additions as new topics land: `determinant.py`, `inverse_matrix.py`, `gaussian_elimination.py`, `eigen.py`, a shared `utils/` module, and `tests/` comparing manual output vs NumPy.

---

## 🛠️ Tech Stack

- **Python 3.x**
- **NumPy** — used only for verification/cross-checking, not as the primary implementation

---

## ▶️ How to Run

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
python matrix_operations/addition_subtraction.py
python matrix_operations/multiplication.py
python matrix_operations/determinant.py
python matrix_operations/inverse_matrix.py
python matrix_operations/gaussian_elimination.py
python matrix_operations/eigen.py
```

Each script is runnable standalone and prints output for each implementation approach alongside a NumPy check, matching how Strang works through problems in lecture.

---

## 🎯 Learning Goals Per Topic

- **Matrix Multiplication:** Understand it as a combination of columns (and rows), not just row×column dot products
- **Determinants:** Connect cofactor expansion to volume scaling and invertibility
- **Inverse Matrices:** Derive inverses via Gauss-Jordan elimination, not `np.linalg.inv()`
- **Gaussian Elimination:** Implement row reduction to solve `Ax = b` systems manually
- **Eigenvalues/Eigenvectors:** Compute via characteristic polynomial for small matrices, then explore power iteration for larger ones

---

## 📚 Learning Source

**Gilbert Strang — *Introduction to Linear Algebra*** (6th Edition)
Companion to MIT OpenCourseWare **18.06 Linear Algebra**

---

## 🗺️ Roadmap

- [ ] Determinants → Inverse → Gaussian Elimination → Eigenvalues
- [ ] Add a shared `utils/` module (validation, printing helpers)
- [ ] Add `tests/` validating manual implementations against NumPy
- [ ] Add visualizations for each transformation (2D/3D) using Matplotlib
- [ ] Extend `eigen.py`'s characteristic-polynomial method beyond 3x3, or generalize to complex eigenvalues
- [ ] Extend to SVD and least-squares (Strang Ch. 7–8) as a stretch goal

---

## 📄 License

MIT License — free to use, modify, and learn from.
