---
name: movefit
version: 1.0
description: "Workspace instructions for the movefit Python package. Use for code changes, tests, packaging, and minimal architecture context."
---

# movefit Workspace Instructions

## Project Overview
- Package: `movefit` (src layout: `src/movefit`).
- Python requirement: `>=3.11`.
- Build backend: `hatchling` via `pyproject.toml`.
- The package currently has no logic outside an empty `__init__.py`.
- No tests are present yet; add tests under `tests/` when introducing behavior.

## Recommended workflows

- Setup:
  - `python -m pip install -e .`
  - `pip install hatchling pytest` (or `python -m pip install -e .[dev]` if you add dev extras).
- Build / check metadata:
  - `python -m hatchling build` (creates `dist/`).
  - `python -m hatchling check`.
- Tests (add tests before relying on this):
  - `python -m pytest`.

## Pixi usage

- `pixi task test` to run test suite (`pytest -q`).
- `pixi task build` to run project build steps (hatchling build).
- `pixi task shell` for interactive environment (if configured by maintainer).

## Troubleshooting

- If dependency resolution fails, run `pixi clean` and re-install (or confirm `pyproject.toml` plus `tool.pixi` sections match expected dependencies).
- If tests fail due to missing environment vars, set them locally (e.g., `export ENV=local`).
- For lint/format issues, apply `black` and `isort` (or as defined in `.github/hooks/pre-commit`).

## Code conventions

- Prefer English for all documentation and comments; exception: raw Excel header names stay in source language.

- Follow idiomatic Python 3.11.
- Keep code small and focused in `src/movefit`.
- Use type hints and documentation for public API in functions/classes.
- Prefer explicit relative imports inside package modules.

## Goals for the AI agent

- Help implement core domain behavior in package modules.
- Add unit tests with `pytest`.
- Keep minimal external dependencies unless justified.
- Suggest package metadata and documentation improvements.

## Agent simplification guidance

- Favor minimal agent set by default:
  - `movefit-coordinator`, `movefit-tests`, `movefit-ci` are usually enough.
  - Add domain-specific agents only when they convey a tangible per-domain rule.
  - Avoid duplicating policy across both `.github/agents/*` and `.github/instructions/*`.
  - Keep variants as `optional` in docs (no requirement for full folder sweep).

## Immediate priorities for contributors

1. Add domain logic to `src/movefit` (e.g., feature modules, services).
2. Add a `tests/` folder and `pytest` coverage.
3. Update `pyproject.toml` with dependencies and optional dev dependencies.

## Guidance for future agent customizations

- If different scopes emerge (CLI, API, ingestion), add specific `*.instructions.md` files under `.github/instructions/` with `applyTo` patterns.
- Add a `.github/hooks/pre-commit` hook to run formatting and static checks.

## Commit message style for agents and humans

- Follow Conventional Commits format in all code/infra commits:
  - `type(scope): subject`
  - body required for non-trivial changes; include causality and testing notes.
  - footer required when referencing issues, release notes, or breaking changes.
- Do not use minimal commit text like `update(docs): adjust docs` without body/footer.

## Agent customization workflow

- Start with `movefit-coordinator` to define the feature and task breakdown.
- Use `movefit-*` agents for implementation (e.g., `movefit-data` for calculations, `movefit-tests` for pytest coverage).
- Keep `.github/agents/<agent>.agent.md` YAML frontmatter in sync with tool permissions and `user-invocable` flags.
- Update `.github/instructions/*.instructions.md` as needed for domain-specific patterns and conventions.

## Example prompts for this workspace

- "Implement a `movefit` package function that computes body-mass-index with type hints and tests."
- "Add a new module `src/movefit/metrics.py` plus `tests/test_metrics.py` with pytest coverage."
- "Update `pyproject.toml` to add `pytest` and `coverage` in `[project.optional-dependencies]`."
- "Create a `.github/workflows/python-package.yml` for CI run test/build/lint steps."
