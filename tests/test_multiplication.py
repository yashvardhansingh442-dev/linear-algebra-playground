import numpy as np
import pytest

from matrix_operations.multiplication import (
    matrix_multiply,
    matrix_multiply_columns,
    matrix_multiply_rows,
)
from tests.conftest import random_matrix

VIEWS = [matrix_multiply, matrix_multiply_columns, matrix_multiply_rows]


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize("m, n, p", [(1, 1, 1), (2, 2, 2), (2, 3, 4), (4, 1, 3), (3, 5, 1)])
def test_matches_numpy(rng, view, m, n, p):
    A, B = random_matrix(rng, m, n), random_matrix(rng, n, p)
    assert view(A, B) == np.matmul(A, B).tolist()


def test_not_commutative():
    A, B = [[1, 2], [3, 4]], [[0, 1], [1, 0]]
    assert matrix_multiply(A, B) != matrix_multiply(B, A)


def test_identity():
    A = [[1, 2], [3, 4]]
    assert matrix_multiply(A, [[1, 0], [0, 1]]) == A


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize("A, B", [
    ([[1, 2, 3]], [[1, 2, 3]]),   # inner dimensions don't match
    ([[1, 2], [3]], [[1], [2]]),  # ragged A
    ([[1]], [[1, 2], [3]]),       # ragged B
    ([], [[1]]),                  # empty
])
def test_bad_input_raises_value_error(view, A, B):
    with pytest.raises(ValueError):
        view(A, B)
