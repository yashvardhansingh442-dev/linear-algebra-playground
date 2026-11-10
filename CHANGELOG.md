# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `CITATION.cff` community and citation files.

### Changed
- Reorganized the flat module folder into a `src/linalg/` package with `core/`, `solvers/`, `spaces/`, and `decompositions/` subpackages.
- Moved lesson-style scripts into `curriculum/` so that explanations are separate from reusable library code.

### Planned
- Property-based tests (Hypothesis) for LU, QR, eigen, and SVD.
- QR decomposition (Gram-Schmidt and Householder) and SVD implementations.
- Docs site (MkDocs Material) and CI workflows for tests and notebooks.
- Benchmarks comparing implementations against NumPy.

## [0.1.0] - 2026-11-10

First tagged release. Core linear algebra implementations written from scratch in Python and verified against NumPy.

### Added
- **Core:** vector and matrix classes, addition, subtraction, and multiplication, determinant, and shared validation utilities.
- **Solvers:** linear system solver, Gaussian elimination, LU decomposition, and matrix inverse.
- **Spaces:** column space and singularity checks.
- **Decompositions:** eigenvalue and eigenvector routines.
- **Curriculum:** lesson scripts on elimination and matrix factorization, and on numerical stability.

[Unreleased]: https://github.com/yashvardhansingh442-dev/linear-algebra-playground/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yashvardhansingh442-dev/linear-algebra-playground/releases/tag/v0.1.0
