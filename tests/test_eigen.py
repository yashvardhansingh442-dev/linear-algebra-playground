import warnings

import numpy as np
import pytest

from matrix_operations.eigen import (
    characteristic_polynomial,
    eigen,
    eigenspace,
    eigenvalues,
    power_iteration,
)
from matrix_operations.utils import mat_vec


def assert_valid_pairs(A, vals, vecs):
    """Every (lambda, v) pair must satisfy A v = lambda v with ||v|| = 1."""
    for lam, v in zip(vals, vecs):
        assert np.linalg.norm(v) == pytest.approx(1.0)
        assert mat_vec(A, v) == pytest.approx([lam * x for x in v], abs=1e-8)


def sym(rng, n):
    """Random symmetric matrix => guaranteed real eigenvalues."""
    M = np.array([[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)], dtype=float)
    return ((M + M.T) / 2).tolist()


def test_characteristic_polynomial_coefficients():
    assert characteristic_polynomial([[4, 1], [2, 3]]) == [1, -7, 10]
    # (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6 for diag(1, 2, 3)
    assert characteristic_polynomial([[1, 0, 0], [0, 2, 0], [0, 0, 3]]) == [1, -6, 11, -6]


@pytest.mark.parametrize("n", [2, 3])
def test_eigenvalues_match_numpy_on_symmetric_matrices(rng, n):
    for _ in range(200):
        A = sym(rng, n)
        assert eigenvalues(A) == pytest.approx(sorted(np.linalg.eigvalsh(A)), abs=1e-7)


@pytest.mark.parametrize("n", [2, 3])
def test_eigenpairs_satisfy_definition(rng, n):
    for _ in range(100):
        A = sym(rng, n)
        vals, vecs = eigen(A)
        assert len(vals) == n  # symmetric => never defective
        assert_valid_pairs(A, vals, vecs)


def test_nonsymmetric_real_eigenvalues():
    A = [[4, 1], [2, 3]]
    vals, vecs = eigen(A)
    assert vals == pytest.approx([2, 5])
    assert_valid_pairs(A, vals, vecs)


# ---- repeated eigenvalues: used to raise a bogus "complex eigenvalues" error ----

@pytest.mark.parametrize("A, expected", [
    ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [1, 1, 1]),            # triple root
    ([[2, 0, 0], [0, 2, 0], [0, 0, 3]], [2, 2, 3]),            # double + simple
    ([[3, 0, 0], [0, 1, 0], [0, 0, 1]], [1, 1, 3]),            # double below simple
    ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0, 0]),            # zero matrix
    ([[5, 0], [0, 5]], [5, 5]),                                 # 2x2 repeated
    ([[2, 1, 0], [0, 2, 1], [0, 0, 2]], [2, 2, 2]),            # Jordan block
])
def test_repeated_eigenvalues(A, expected):
    assert eigenvalues(A) == pytest.approx(expected, abs=1e-8)


def test_identity_has_a_full_eigenbasis():
    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    vals, vecs = eigen(I)
    assert vals == pytest.approx([1, 1, 1])
    assert np.linalg.matrix_rank(np.array(vecs)) == 3  # three *different* vectors
    assert_valid_pairs(I, vals, vecs)


def test_repeated_eigenvalue_with_full_eigenspace():
    A = [[2, 0, 0], [0, 2, 0], [0, 0, 3]]
    vals, vecs = eigen(A)
    assert vals == pytest.approx([2, 2, 3])
    assert np.linalg.matrix_rank(np.array(vecs)) == 3
    assert_valid_pairs(A, vals, vecs)
    assert len(eigenspace(A, 2)) == 2


def test_defective_matrix_reports_fewer_eigenvectors_than_n():
    A = [[2, 1], [0, 2]]
    vals, vecs = eigen(A)
    assert vals == pytest.approx([2])  # only one independent eigenvector
    assert_valid_pairs(A, vals, vecs)


def test_eigenspace_rejects_non_eigenvalue():
    with pytest.raises(ValueError, match="not an eigenvalue"):
        eigenspace([[4, 1], [2, 3]], 7)


# ---- error handling ----

@pytest.mark.parametrize("A", [
    [[0, -1], [1, 0]],                          # 90-degree rotation: +-i
    [[0, -1, 0], [1, 0, 0], [0, 0, 1]],         # rotation about z: 1, +-i
])
def test_complex_eigenvalues_raise(A):
    with pytest.raises(ValueError, match="complex"):
        eigenvalues(A)


def test_large_matrices_not_supported_by_char_poly():
    with pytest.raises(NotImplementedError):
        eigenvalues(np.eye(4))


@pytest.mark.parametrize("A", [[[1, 2, 3], [4, 5, 6]], [[1, 2], [3]], []])
def test_bad_input_raises_value_error(A):
    with pytest.raises(ValueError):
        eigenvalues(A)


# ---- power iteration ----

@pytest.mark.parametrize("n", [2, 3, 5, 8])
def test_power_iteration_finds_dominant_eigenpair(rng, n):
    for _ in range(20):
        A = sym(rng, n)
        true_vals = np.linalg.eigvalsh(A)
        top, second = sorted(true_vals, key=abs, reverse=True)[:2]
        if abs(abs(top) - abs(second)) < 0.5:  # near-tie => slow/no convergence
            continue
        lam, v = power_iteration(A, num_iterations=5000)
        assert lam == pytest.approx(top, abs=1e-6)
        assert mat_vec(A, v) == pytest.approx([lam * x for x in v], abs=1e-5)


def test_power_iteration_handles_negative_dominant_eigenvalue():
    lam, v = power_iteration([[-5, 0], [0, 1]])
    assert lam == pytest.approx(-5)


def test_power_iteration_survives_start_vector_orthogonal_to_old_default():
    # Old default start [1, 1] is the *null* vector of this matrix (eigenvalue 0),
    # so the dominant eigenvalue 2 was missed / division by zero.
    lam, _ = power_iteration([[1, -1], [-1, 1]])
    assert lam == pytest.approx(2)


def test_power_iteration_zero_matrix():
    lam, _ = power_iteration([[0, 0], [0, 0]])
    assert lam == 0.0


def test_power_iteration_warns_when_it_cannot_converge():
    # Eigenvalues +1 and -1 tie for "dominant"; a generic start oscillates.
    with pytest.warns(RuntimeWarning, match="did not converge"):
        power_iteration([[0, 1], [1, 0]], num_iterations=50, start=[1, 0])


def test_power_iteration_rejects_bad_arguments():
    with pytest.raises(ValueError):
        power_iteration([[1, 0], [0, 1]], num_iterations=0)
    with pytest.raises(ValueError):
        power_iteration([[1, 0], [0, 1]], start=[1, 2, 3])
    with pytest.raises(ValueError):
        power_iteration([[1, 2, 3], [4, 5, 6]])


def test_no_warning_on_normal_convergence():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        power_iteration([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])


def test_triangular_matrices_with_repeated_eigenvalues(rng):
    """Triangular => eigenvalues are exactly the diagonal, repeats and defective cases included."""
    for _ in range(300):
        d = [rng.choice([-2, -1, 0, 1, 2, 3]) for _ in range(3)]
        U = [
            [d[0], rng.randint(-3, 3), rng.randint(-3, 3)],
            [0, d[1], rng.randint(-3, 3)],
            [0, 0, d[2]],
        ]
        assert eigenvalues(U) == pytest.approx(sorted(d), abs=1e-6)
        vals, vecs = eigen(U)
        assert_valid_pairs(U, vals, vecs)
