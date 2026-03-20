---
name: movefit-tests
description: "Use when editing tests/ and adding new test coverage for movefit behavior."
applyTo: "tests/**/*.py"
---

- Write tests for new behavior before implementation when possible.
- Use pytest fixtures and parametrization, keep tests clear and independent.
- Focus on core domain logic and edge cases, not implementation internals.
- Run `python -m pytest --maxfail=1 -q` locally before PR.
- Add a new `tests/test_*.py` file per new module in src/movefit.
