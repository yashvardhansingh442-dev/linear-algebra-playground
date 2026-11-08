"""
Shared helpers: input validation, tolerances, and pretty-printing.

Every public routine in this package funnels its inputs through
`as_matrix` / `as_vector`, so the "fail loudly" behaviour (empty input,
ragged rows, wrong shapes, NaN/inf) is implemented once, here.

NumPy arrays are accepted as input for convenience and converted to plain
lists of lists -- the algorithms themselves never touch NumPy.
"""
import math
import numbers
import sys

EPS = sys.float_info.epsilon  # ~2.2e-16, machine epsilon for float64


def _to_nested_list(M):
    """Convert numpy arrays (or anything with .tolist()) to nested lists."""
    return M.tolist() if hasattr(M, "tolist") else M


def as_matrix(M, name="Matrix"):
    """
    Validate M and return a fresh list-of-lists copy (the caller's data is
    never mutated). Raises ValueError for empty, ragged, non-2D or
    non-finite input.
    """
    M = _to_nested_list(M)
    if not isinstance(M, (list, tuple)) or len(M) == 0:
        raise ValueError(f"{name} cannot be empty.")
    rows = []
    for row in M:
        row = _to_nested_list(row)
        if not isinstance(row, (list, tuple)):
            raise ValueError(f"{name} must be a 2D list of rows.")
        rows.append(list(row))
    width = len(rows[0])
    if width == 0:
        raise ValueError(f"{name} cannot be empty.")
    if any(len(row) != width for row in rows):
        raise ValueError(f"{name} is not rectangular.")
    for row in rows:
        for x in row:
            if isinstance(x, bool) or not isinstance(x, numbers.Real):
                raise ValueError(f"{name} must contain only real numbers, got {x!r}.")
            if not math.isfinite(x):
                raise ValueError(f"{name} contains a non-finite value ({x}).")
    return rows


def as_vector(v, name="Vector"):
    """Validate a 1D vector and return a fresh list copy."""
    v = _to_nested_list(v)
    if not isinstance(v, (list, tuple)) or len(v) == 0:
        raise ValueError(f"{name} cannot be empty.")
    out = list(v)
    for x in out:
        if isinstance(x, bool) or not isinstance(x, numbers.Real):
            raise ValueError(f"{name} must contain only real numbers, got {x!r}.")
        if not math.isfinite(x):
            raise ValueError(f"{name} contains a non-finite value ({x}).")
    return out


def shape(M):
    """(rows, cols) of an already-validated matrix."""
    return len(M), len(M[0])


def as_square_matrix(M, operation="This operation", name="Matrix"):
    """Like as_matrix, but also requires rows == cols."""
    M = as_matrix(M, name)
    rows, cols = shape(M)
    if rows != cols:
        raise ValueError(f"{operation} requires a square matrix, got {rows}x{cols}.")
    return M


def identity(n):
    """n x n identity matrix as a list of lists of floats."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def max_abs(M):
    """Largest absolute entry of a matrix (used to scale tolerances)."""
    return max(abs(x) for row in M for x in row)


def pivot_tolerance(M, tol=None):
    """
    Absolute threshold below which a pivot counts as zero.

    Scaled by the matrix size and its largest entry, the same idea used by
    LAPACK / NumPy's matrix_rank: n * eps * max|a_ij|. Pass `tol` to
    override it with an explicit absolute value.
    """
    if tol is not None:
        return tol
    return len(M) * EPS * max_abs(M)


def mat_vec(A, v):
    """Matrix-vector product A @ v for plain lists."""
    return [sum(a * x for a, x in zip(row, v)) for row in A]


def norm(v):
    """Euclidean (2-norm) length of a vector."""
    return math.sqrt(sum(x * x for x in v))


def print_matrix(M, name=None, precision=4):
    """Print a matrix one row per line, rounding floats for readability."""
    if name:
        print(f"{name}:")
    for row in M:
        print("  [" + ", ".join(_fmt(x, precision) for x in row) + "]")


def _fmt(x, precision):
    if isinstance(x, float):
        r = round(x, precision)
        return f"{(0.0 if r == 0 else r):g}"  # avoids printing -0
    return str(x)
