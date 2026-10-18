import numpy as np
import pytest

from matrix_operations.addition_subtraction import matrix_add, matrix_subtract
from tests.conftest import random_matrix


def test_basic():
    assert matrix_add([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]
    assert matrix_subtract([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[-4, -4], [-4, -4]]


@pytest.mark.parametrize("shape", [(1, 1), (1, 4), (3, 1), (3, 5)])
def test_matches_numpy(rng, shape):
    A, B = random_matrix(rng, *shape), random_matrix(rng, *shape)
    assert matrix_add(A, B) == np.add(A, B).tolist()
    assert matrix_subtract(A, B) == np.subtract(A, B).tolist()


def test_does_not_mutate_inputs():
    A, B = [[1, 2]], [[3, 4]]
    matrix_add(A, B)
    assert A == [[1, 2]] and B == [[3, 4]]


def test_accepts_numpy_arrays():
    assert matrix_add(np.eye(2), np.eye(2)) == [[2.0, 0.0], [0.0, 2.0]]


@pytest.mark.parametrize("A, B", [
    ([[1, 2]], [[1], [2]]),         # transposed shapes
    ([[1, 2], [3, 4]], [[1, 2]]),   # row count differs
    ([[1, 2], [3]], [[1, 2], [3, 4]]),  # ragged
    ([], []),                        # empty
    ([[1, float("nan")]], [[1, 2]]),  # non-finite
])
def test_bad_input_raises_value_error(A, B):
    with pytest.raises(ValueError):
        matrix_add(A, B)
    with pytest.raises(ValueError):
        matrix_subtract(A, B)
