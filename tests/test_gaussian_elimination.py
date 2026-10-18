import numpy as np
import pytest

from matrix_operations.gaussian_elimination import (
    back_substitution,
    forward_elimination,
    solve,
)
from tests.conftest import random_matrix


def test_known_system():
    x = solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])
    assert x == pytest.approx([2, 3, -1])


@pytest.mark.parametrize("n", [1, 2, 3, 5, 8])
def test_random_systems_match_numpy(rng, n):
    for _ in range(10):
        A = random_matrix(rng, n, n)
        if abs(np.linalg.det(A)) < 1e-6:
            continue
        b = [rng.randint(-9, 9) for _ in range(n)]
        assert solve(A, b) == pytest.approx(np.linalg.solve(A, b), abs=1e-8)


def test_zero_pivot_needs_row_swap():
    assert solve([[0, 1], [1, 0]], [2, 3]) == pytest.approx([3, 2])


def test_forward_elimination_gives_upper_triangular():
    aug = forward_elimination([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], [5, -2, 9])
    for i in range(3):
        for j in range(i):
            assert aug[i][j] == pytest.approx(0, abs=1e-12)
    assert back_substitution(aug) == pytest.approx([1, 1, 2])


def test_does_not_mutate_inputs():
    A, b = [[2, 1], [1, 3]], [1, 2]
    solve(A, b)
    assert A == [[2, 1], [1, 3]] and b == [1, 2]


def test_accepts_numpy_arrays():
    assert solve(np.array([[2.0, 1.0], [1.0, 3.0]]), np.array([1.0, 2.0])) == pytest.approx(
        np.linalg.solve([[2, 1], [1, 3]], [1, 2])
    )


def test_exactly_singular_raises():
    with pytest.raises(ValueError, match="singular"):
        solve([[1, 2], [2, 4]], [3, 6])


def test_numerically_singular_raises_instead_of_returning_garbage():
    # Rows are parallel up to one ulp; naive "== 0" pivot checks return ~1e16.
    with pytest.raises(ValueError, match="singular"):
        solve([[1, 2], [1, 2.0000000000000004]], [3, 6])


def test_hilbert_matrix_is_ill_conditioned_but_not_singular():
    n = 6
    H = [[1 / (i + j + 1) for j in range(n)] for i in range(n)]
    x_true = [1.0] * n
    b = (np.array(H) @ np.array(x_true)).tolist()
    assert solve(H, b) == pytest.approx(x_true, rel=1e-5)


@pytest.mark.parametrize("A, b", [
    ([[1, 2, 3], [4, 5, 6]], [1, 2]),  # not square
    ([[1, 2], [3, 4]], [1, 2, 3]),     # b too long
    ([[1, 2], [3]], [1, 2]),           # ragged
    ([], []),                          # empty
])
def test_bad_input_raises_value_error(A, b):
    with pytest.raises(ValueError):
        solve(A, b)
