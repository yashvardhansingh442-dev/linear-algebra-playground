# linear-algebra-playground: common developer tasks
# Run `make` or `make help` to see everything available.
# NOTE: recipe lines must be indented with a TAB character, not spaces.

PYTHON ?= python
PIP    := $(PYTHON) -m pip

.DEFAULT_GOAL := help

.PHONY: help install install-dev install-all hooks \
        test test-fast doctest notebooks cov \
        lint format format-check typecheck check \
        docs docs-serve bench build clean

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
install:  ## Install the library only
	$(PIP) install -e .

install-dev:  ## Install library + dev tools + notebook support
	$(PIP) install -e ".[dev,notebooks]"
	$(MAKE) hooks

install-all:  ## Install everything (dev, notebooks, docs)
	$(PIP) install -e ".[all]"
	$(MAKE) hooks

hooks:  ## Install pre-commit git hooks
	pre-commit install

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------
test:  ## Run the full test suite
	pytest

test-fast:  ## Run everything except slow tests
	pytest -m "not slow"

doctest:  ## Run the examples inside docstrings
	pytest --doctest-modules src/

notebooks:  ## Execute all curriculum notebooks (fails if any cell errors)
	pytest --nbmake curriculum/

cov:  ## Run tests with a coverage report
	pytest --cov --cov-report=term-missing --cov-report=html
	@echo "HTML report: htmlcov/index.html"

# ---------------------------------------------------------------------------
# Code quality
# ---------------------------------------------------------------------------
lint:  ## Lint with ruff
	ruff check .

format:  ## Auto-format code with ruff
	ruff check --fix .
	ruff format .

format-check:  ## Check formatting without changing files (used in CI)
	ruff format --check .

typecheck:  ## Type-check src/ with mypy
	mypy src/

check: lint format-check typecheck test  ## Run everything CI runs

# ---------------------------------------------------------------------------
# Docs, benchmarks, packaging
# ---------------------------------------------------------------------------
docs:  ## Build the documentation site
	mkdocs build -f docs/mkdocs.yml

docs-serve:  ## Serve docs locally with live reload
	mkdocs serve -f docs/mkdocs.yml

bench:  ## Run the solver benchmark (NumPy/SciPy vs each other)
	$(PYTHON) explorations/solver_benchmark.py

build:  ## Build the sdist and wheel
	$(PYTHON) -m build

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
clean:  ## Remove build artifacts and caches
	rm -rf build dist *.egg-info src/*.egg-info site htmlcov .coverage
	rm -rf .pytest_cache .mypy_cache .ruff_cache .hypothesis
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} +
