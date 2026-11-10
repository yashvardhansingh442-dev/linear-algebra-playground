---
name: Bug report
about: "Report incorrect results, crashes, or broken code in the library or notebooks"
title: "[Bug] "
labels: ["bug"]
assignees: []
---

<!--
Thanks for taking the time to report a bug! The more specific you are, the faster it can be fixed.
If an explanation is confusing but nothing is actually wrong, please use the
"Explanation unclear" template instead. For math errors in the lessons, use this one.
-->

## What type of problem is this?

<!-- Delete the ones that don't apply. -->

- [ ] Wrong numerical result (function returns an incorrect answer)
- [ ] Crash or exception (function raises an error it shouldn't)
- [ ] Math error in an explanation, proof, or exercise solution
- [ ] Notebook fails to run
- [ ] Test or CI failure
- [ ] Other

## Where does it happen?

<!-- File path, function name, or notebook and section. Example: `src/linalg/solvers/lu.py`, `lu_decompose()` -->

## Description

<!-- A clear and concise description of what is wrong. -->

## Minimal example to reproduce

<!--
Please give the smallest example that shows the problem, including the exact input matrix or vector.
Small matrices (2x2 or 3x3) are ideal. Set a random seed if randomness is involved.
-->

```python
import numpy as np
from linalg.solvers.lu import lu_decompose

A = np.array([[1.0, 2.0],
              [3.0, 4.0]])

L, U, P = lu_decompose(A)
print(L, U, P)
```

## Expected behavior

<!--
What should happen? If you know the correct answer, show how you got it
(for example, the result from `numpy.linalg` or a hand calculation).
-->

```text
Expected output here
```

## Actual behavior

<!-- What happened instead? Paste the full error message or wrong output. -->

```text
Actual output or full traceback here
```

## Numerical details (if the result is slightly off)

<!-- Delete this section if the result is completely wrong or it crashed. -->

- Condition number of the input (`np.linalg.cond(A)`):
- Size of the error (for example `np.linalg.norm(A - L @ U)`):
- Is the matrix singular or nearly singular?  yes / no / not sure

## Environment

<!-- Run `python -c "import sys, numpy; print(sys.version); print(numpy.__version__)"` and fill this in. -->

- Operating system:
- Python version:
- NumPy version:
- `linalg` version or commit (`pip show linalg` or `git rev-parse --short HEAD`):
- How did you install it? (`pip install -e .`, copied files, other):

## Additional context

<!-- Screenshots, related issues, or anything else that might help. -->

## Checklist

- [ ] I searched existing issues and did not find a duplicate
- [ ] I am using the latest version of the `main` branch
- [ ] My example runs on its own (no other files needed)
- [ ] I'm willing to help fix this, or I would like someone to guide me through fixing it (optional)
