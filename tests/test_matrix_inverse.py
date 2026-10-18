import numpy as np
import pytest

from matrix_operations.matrix_inverse import inverse
from matrix_operations.multiplication import matrix_multiply
from tests.conftest import random_matrix


def test_known_inverse():
    assert inverse([[2, 1], [1, 1]]) == pytest.approx(np.array([[1, -1], [-1, 2]]))


@pytest.mark.parametrize("n", [1, 2, 3, 4, 6])
def test_random_matrices_match_numpy_and_give_identity(rng, n):
    for _ in range(10):
        A = random_matrix(rng, n, n)
        if abs(np.linalg.det(A)) < 1e-6:
            continue
        inv = inverse(A)
        assert inv == pytest.approx(np.linalg.inv(A), abs=1e-8)
        assert matrix_multiply(A, inv) == pytest.approx(np.eye(n), abs=1e-8)


def test_needs_row_swap():
    A = [[0, 2, 1], [1, 1, 0], [2, 0, 3]]
    assert inverse(A) == pytest.approx(np.linalg.inv(A))


def test_inverse_of_inverse_is_original():
    A = [[4, 7], [2, 6]]
    assert inverse(inverse(A)) == pytest.approx(np.array(A))


def test_product_rule_reverses_order():
    A, B = [[2, 1], [1, 1]], [[0, 1], [1, 2]]
    AB = matrix_multiply(A, B)
    assert inverse(AB) == pytest.approx(np.array(matrix_multiply(inverse(B), inverse(A))))


def test_does_not_mutate_input():
    A = [[2, 1], [1, 1]]
    inverse(A)
    assert A == [[2, 1], [1, 1]]


@pytest.mark.parametrize("A", [
    [[1, 2], [2, 4]],
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[0, 0], [0, 0]],
])
def test_singular_raises(A):
    with pytest.raises(ValueError, match="singular"):
        inverse(A)


@pytest.mark.parametrize("A", [[[1, 2, 3], [4, 5, 6]], [[1, 2], [3]], []])
def test_bad_input_raises_value_error(A):
    with pytest.raises(ValueError):
        inverse(A)
