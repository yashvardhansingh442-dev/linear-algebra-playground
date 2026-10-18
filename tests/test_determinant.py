import numpy as np
import pytest

from matrix_operations.determinant import determinant, determinant_elimination
from tests.conftest import random_matrix


def test_known_values():
    assert determinant([[7]]) == 7
    assert determinant([[1, 2], [3, 4]]) == -2
    assert determinant([[6, 1, 1], [4, -2, 5], [2, 8, 7]]) == -306


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_both_methods_match_numpy(rng, n):
    for _ in range(10):
        M = random_matrix(rng, n, n)
        expected = np.linalg.det(M)
        assert determinant(M) == pytest.approx(expected, abs=1e-6)
        assert determinant_elimination(M) == pytest.approx(expected, abs=1e-6)


def test_cofactor_is_exact_for_integers(rng):
    M = random_matrix(rng, 4, 4)
    assert determinant(M) == round(np.linalg.det(M))


def test_singular_matrices_have_zero_determinant():
    assert determinant([[1, 2], [2, 4]]) == 0
    assert determinant_elimination([[1, 2], [2, 4]]) == 0
    assert determinant_elimination([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0


def test_row_swap_flips_sign():
    A = [[1, 2], [3, 4]]
    swapped = [A[1], A[0]]
    assert determinant_elimination(swapped) == pytest.approx(-determinant_elimination(A))


def test_zero_pivot_requires_swap():
    # Top-left entry is 0, so elimination must swap rows to proceed.
    assert determinant_elimination([[0, 1], [1, 0]]) == pytest.approx(-1)


def test_product_rule(rng):
    A, B = random_matrix(rng, 3, 3), random_matrix(rng, 3, 3)
    AB = (np.array(A) @ np.array(B)).tolist()
    assert determinant(AB) == determinant(A) * determinant(B)


@pytest.mark.parametrize("fn", [determinant, determinant_elimination])
@pytest.mark.parametrize("M", [[[1, 2, 3], [4, 5, 6]], [[1, 2], [3]], []])
def test_bad_input_raises_value_error(fn, M):
    with pytest.raises(ValueError):
        fn(M)
