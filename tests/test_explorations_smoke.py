"""
The scripts in explorations/ are NumPy/SciPy demos, not library code, so
they get a smoke test only: each one must run top to bottom without raising.
"""
import runpy
from pathlib import Path

import pytest

pytest.importorskip("numpy")
pytest.importorskip("scipy")

SCRIPTS = sorted((Path(__file__).parent.parent / "explorations").glob("*.py"))


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_exploration_script_runs(script, capsys):
    runpy.run_path(str(script), run_name="__main__")
    assert capsys.readouterr().out  # every script prints its results
