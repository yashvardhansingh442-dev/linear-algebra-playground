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
| 3 | Matrix Multiplication (incl. row/column view) | Lecture 1–3 | 🔲 In Progress |
| 4 | Determinants (cofactor expansion) | Lecture 18–19 | 🔲 Planned |
| 5 | Inverse Matrices (Gauss-Jordan method) | Lecture 3 | 🔲 Planned |
| 6 | Gaussian Elimination (row echelon + back-substitution) | Lecture 2 | 🔲 Planned |
| 7 | Eigenvalues & Eigenvectors (characteristic polynomial, power iteration) | Lecture 21–22 | 🔲 Planned |

---

## ✅ Progress Tracker

- [x] Matrix Addition
- [x] Matrix Subtraction
- [ ] Matrix Multiplication
- [ ] Determinant
- [ ] Inverse
- [ ] Gaussian Elimination
- [ ] Eigenvalues

**Current focus:** Matrix Multiplication (dot-product, row-picture, and column-picture implementations)

---

## 📂 Repository Structure

```
linear-algebra-playground/
│
├── matrix_addition.py
├── matrix_subtraction.py
├── matrix_multiplication.py       # in progress
├── determinant.py                 # planned
├── inverse_matrix.py              # planned
├── gaussian_elimination.py        # planned
├── eigen.py                       # planned
│
├── utils/
│   └── matrix_helpers.py          # shared helper functions (validation, printing, etc.)
│
├── visualizations/
│   └── plots.py                   # matplotlib-based vector/transformation plots
│
├── tests/
│   └── test_*.py                  # unit tests comparing manual output vs NumPy
│
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.x**
- **NumPy** — used only for verification/cross-checking, not as the primary implementation
- **Matplotlib** — for visualizing vectors, transformations, and eigenvector directions

---

## ▶️ How to Run

```bash
git clone https://github.com/yashvardhansingh442-dev/linear-algebra-playground.git
cd linear-algebra-playground
pip install -r requirements.txt
python matrix_addition.py
```

Each script is runnable standalone and prints a step-by-step breakdown of the computation (not just the final result) — matching how Strang works through problems in lecture.

---

## 🎯 Learning Goals Per Topic

- **Matrix Multiplication:** Understand it as a combination of columns, not just row×column dot products
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

- [ ] Finish core topics (multiplication → eigenvalues)
- [ ] Add visualizations for each transformation (2D/3D)
- [ ] Add unit tests validating manual implementations against NumPy
- [ ] Extend to SVD and least-squares (Strang Ch. 7–8) as a stretch goal

---

## 📄 License

MIT License — free to use, modify, and learn from.
