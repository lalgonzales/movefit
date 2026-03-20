---
name: movefit-python
description: "Use when editing Python code in src/movefit; enforce package conventions, typing, and tests."
applyTo: "src/movefit/**/*.py"
---

- Keep modules small and focused.
- Use Python 3.11 idioms and type hints for public API.
- Prefer explicit relative imports within movefit.
- Add or update `tests/` when implementing behavior.
- Use `python -m pytest` and aim for fast deterministic tests.
- Avoid external dependencies unless needed; keep minimal.
