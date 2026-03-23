# movefit-qa skill

This skill enforces project code style and docs checklist for movefit.

## Purpose
- Ensure code style and quality rules are followed in PRs.
- Check for docs updates when behavioral or API changes occur.

## Rules
1. Static style checks:
   - `black --check .`
   - `isort --check-only .`
   - `ruff check .` (when configured)
   - `python -m pytest -q` and `pixi task test`
2. Docs checks:
   - any new API route, schema, or user-facing behavior must include docs in `README.md` or `docs/`.
   - code comments and docstrings should exist for public functions/classes.
3. CI readiness:
   - suggest adding minimal GitHub action config if absent.
   - verify `pyproject.toml` has dev extras for testing and linting.

## Example PR gate phrase
- "Run style checks and tests locally; confirm docs sections are updated for any new endpoint."