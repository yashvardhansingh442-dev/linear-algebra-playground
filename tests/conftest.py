import random

import pytest


@pytest.fixture
def rng():
    """Seeded RNG so any failure is reproducible."""
    return random.Random(42)


def random_matrix(rng, rows, cols, lo=-5, hi=5):
    return [[rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]
