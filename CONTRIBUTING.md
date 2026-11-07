# Contributing to linear-algebra-playground

Thanks for wanting to help! This project is a learning resource for linear algebra: explanations, from-scratch Python code, visuals, and exercises, following the progression of MIT 18.06. Contributions of every size are welcome, from fixing a typo to writing a whole new unit.

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Contributing Code](#contributing-code)
- [Contributing Learning Content](#contributing-learning-content)
- [Contributing Exercises](#contributing-exercises)
- [Notebook Guidelines](#notebook-guidelines)
- [Testing](#testing)
- [Style Guide](#style-guide)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Credit and Copyright](#credit-and-copyright)

## Ways to Contribute

| You want to... | Do this |
|---|---|
| Fix a typo or unclear sentence | Open a small PR directly |
| Report a math error or bug | Open an issue (bug report template) |
| Say an explanation is confusing | Open an issue (explanation unclear template) |
| Suggest a new topic | Open an issue (topic request template) |
| Add or improve code in `src/linalg/` | Follow [Contributing Code](#contributing-code) |
| Write or improve a unit in `curriculum/` | Follow [Contributing Learning Content](#contributing-learning-content) |
| Add practice problems | Follow [Contributing Exercises](#contributing-exercises) |
| Add a visualization or animation | Open a PR, put images in `assets/` |

Not sure where to start? Look for issues labeled `good first issue` or `help wanted`.

## Getting Started

**1. Fork and clone**

```bash
git clone https://github.com/<your-username>/linear-algebra-playground.git
cd linear-algebra-playground
```

**2. Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

**3. Install in editable mode with dev tools**

```bash
pip install -e ".[dev,notebooks]"
pre-commit install
```

**4. Check everything works**

```bash
pytest
```

If all tests pass, you're ready.

## Project Structure

```
src/linalg/        # the installable library (from-scratch implementations)
tests/             # unit, property-based, and numerical stability tests
curriculum/        # the learning content, one folder per unit
projects/          # larger capstone projects
benchmarks/        # comparisons against NumPy
docs/              # documentation site (MkDocs)
assets/            # images, GIFs, diagrams
```

The rule of thumb: **explanations and tutorials live in `curriculum/`; reusable, tested code lives in `src/linalg/`.** Notebooks should import from the library rather than redefine functions.

## Development Workflow

1. Check existing issues and PRs to avoid duplicate work. For anything larger than a small fix, open an issue first to discuss.
2. Create a branch from `main`:
   ```bash
   git checkout -b feat/svd-implementation
   ```
   Use prefixes: `feat/`, `fix/`, `docs/`, `test/`, `refactor/`.
3. Make your changes in small, focused commits.
4. Run the checks locally (see [Testing](#testing)).
5. Push and open a pull request.

## Contributing Code

All library code lives in `src/linalg/`.

**Requirements for new or changed code:**

- **From scratch first.** Core implementations must not call `numpy.linalg` or `scipy.linalg` to do the thing being taught. NumPy arrays for storage and basic arithmetic are fine. NumPy and SciPy are used in tests and comparison notebooks to *verify* results.
- **Type hints** on all public functions.
- **Docstrings** in NumPy style, including a short math description, complexity, and an example:

  ```python
  def lu_decompose(A, pivoting=True):
      """Compute PA = LU.

      Parameters
      ----------
      A : ndarray of shape (n, n)
          Square input matrix.
      pivoting : bool, default True
          Use partial pivoting for numerical stability.

      Returns
      -------
      L, U, P : ndarray
          Lower, upper, and permutation matrices with PA = LU.

      Math
      ----
      Elimination as a product of elementary matrices: E_k ... E_1 A = U.

      Complexity
      ----------
      O(2n^3 / 3) floating point operations.

      Examples
      --------
      >>> L, U, P = lu_decompose(A)
      """
  ```
- **Input validation** with clear errors (non-square matrix, shape mismatch, singular matrix). Use the helpers in `core/validation.py`.
- **Tests** for every new function (see below).
- **No new dependencies** without discussing it in an issue first.

## Contributing Learning Content

Each unit in `curriculum/` follows the same template so learners always know where to look:

```
NN-unit-name/
├── README.md              # goals, prerequisites, time estimate, outline
├── 1-intuition.md         # geometric meaning first, formulas later
├── 2-theory.md            # definitions, theorems, proofs
├── 3-from-scratch.ipynb   # step-by-step implementation with visuals
├── 4-numpy-compare.ipynb  # verification against NumPy/SciPy
├── 5-pitfalls.md          # common mistakes and numerical issues
├── 6-applications.md      # where it shows up (ML, robotics, physics)
├── exercises/
│   ├── problems.md
│   ├── solutions.md
│   └── coding_tasks.py
├── quiz.md
└── further-reading.md
```

**Writing guidelines:**

- **Intuition before formalism.** Start with a picture or concrete example, then generalize.
- **Plain language.** Define every term the first time you use it. Add new terms to `docs/glossary.md`.
- **Small steps.** If a derivation skips a step, add it. "It can be shown that..." is a red flag.
- **Use your own words.** Do not copy lecture notes, textbooks, or solutions. Link to the source instead.
- **Show, then tell.** Prefer a plot or worked example over a paragraph of description.
- **Be honest about difficulty.** Mark optional or advanced sections clearly.
- Write math in LaTeX (`$...$` inline, `$$...$$` for display). Keep symbols consistent with the glossary.

## Contributing Exercises

Good exercises are tiered:

- **Warm-up:** checks the definition (a minute or two).
- **Core:** requires applying the idea (5 to 15 minutes).
- **Challenge:** requires combining ideas or a short proof.

Every exercise needs a solution in `solutions.md` that explains the reasoning, not just the final answer. Coding tasks in `coding_tasks.py` should be fill-in-the-blank functions paired with tests that fail until the learner solves them. Do not submit solutions to graded coursework from any university.

## Notebook Guidelines

- **Strip outputs before committing.** The `nbstripout` pre-commit hook does this automatically; make sure `pre-commit install` was run.
- **Notebooks must run top to bottom** on a fresh kernel. CI executes every notebook and fails if any cell errors.
- **Set random seeds** (`np.random.seed(42)` or `default_rng(42)`) so results are reproducible.
- **Keep logic in the library.** Notebooks explain and visualize; they should not contain big blocks of reusable code.
- **One idea per section,** with a short markdown cell explaining what and why before each code cell.
- Keep file sizes small. Don't commit large datasets; put small ones in `data/` with a README noting their source and license.
- Label plot axes, add titles, and make sure figures are readable in dark and light themes.

## Testing

Run everything:

```bash
pytest
```

Useful variants:

```bash
pytest tests/unit                 # fast, hand-verified examples
pytest tests/property             # Hypothesis property-based tests
pytest tests/numerical            # ill-conditioned and edge cases
pytest --doctest-modules src/     # run docstring examples
pytest --nbmake curriculum/       # execute notebooks
```

**What to test:**

- **Unit tests:** small matrices with known, hand-computed answers.
- **Property tests:** mathematical properties on random inputs, such as `Q.T @ Q ≈ I` for QR, `A ≈ L @ U` for LU, `A @ v ≈ λ * v` for eigenpairs, `U @ S @ Vt ≈ A` for SVD.
- **Numerical tests:** singular and near-singular matrices, Hilbert matrices, large condition numbers, empty and 1x1 inputs.
- **Comparison tests:** results agree with NumPy/SciPy within a stated tolerance (use `np.allclose` or `np.testing.assert_allclose`, never `==` on floats).

New features without tests will not be merged.

## Style Guide

We use automated tooling so you don't have to think about formatting.

```bash
ruff check .          # lint
ruff format .         # format
mypy src/             # type check
```

`pre-commit` runs these on every commit. To run all hooks manually:

```bash
pre-commit run --all-files
```

General conventions:

- Python 3.10 or newer.
- `snake_case` for functions and variables, `PascalCase` for classes.
- Line length 88.
- Descriptive names. Prefer `pivot_row` over `pr`. Where a name mirrors math notation (`A`, `L`, `U`, `Q`), explain it in the docstring.
- Markdown: one sentence per line is fine, wrap at your discretion, use fenced code blocks with a language tag.

## Commit Messages

Use short, descriptive messages in the imperative mood, following [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(solvers): add LU decomposition with partial pivoting
fix(qr): handle zero columns in Gram-Schmidt
docs(curriculum): add intuition section for eigenvalues
test(svd): add property tests for reconstruction
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`.

## Pull Request Process

1. Make sure all checks pass locally: `pytest`, `ruff check .`, `mypy src/`.
2. Update documentation, the glossary, and the curriculum table in `README.md` if relevant.
3. Add an entry to `CHANGELOG.md` under "Unreleased".
4. Open the PR against `main` and fill in the template: what changed, why, and how you tested it. Link the related issue (`Closes #12`).
5. Keep PRs focused. One feature or fix per PR is much easier to review.
6. A maintainer will review, usually within a week. Expect questions and requests for changes; they are part of the process and not criticism. Respond in the PR thread, push updates to the same branch.
7. Once approved and CI is green, a maintainer will merge.

**Review checklist (for contributors and reviewers):**

- [ ] Math is correct and clearly explained
- [ ] Code is from scratch where required, and tested
- [ ] Docstrings and type hints present
- [ ] Notebooks run top to bottom with outputs stripped
- [ ] No copied or uncredited material
- [ ] CI passes

## Reporting Issues

Use the issue templates:

- **Bug report:** include what you expected, what happened, a minimal example, and your OS and Python version.
- **Explanation unclear:** tell us which file and section confused you and what you were expecting to understand. This is one of the most valuable kinds of feedback.
- **Topic request:** describe the topic and why it would help learners.

For security concerns or conduct issues, don't open a public issue. See the Reporting section of the [Code of Conduct](CODE_OF_CONDUCT.md).

## Credit and Copyright

- By contributing, you agree that your contributions are licensed under the project's [MIT License](LICENSE).
- Only submit work you wrote or have permission to share.
- Do not copy text, figures, or solutions from textbooks, MIT OpenCourseWare, or other sources. Summarize in your own words and link to the original.
- Disclose substantial AI assistance in your PR description, and verify the math and code yourself.
- Contributors are credited in the repository's contributor list and in release notes.

---

Questions? Open a discussion or an issue. Thank you for helping make linear algebra easier to learn!
