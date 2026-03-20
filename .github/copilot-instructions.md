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

## Code conventions

- Follow idiomatic Python 3.11.
- Keep code small and focused in `src/movefit`.
- Use type hints and documentation for public API in functions/classes.
- Prefer explicit relative imports inside package modules.

## Goals for the AI agent

- Help implement core domain behavior in package modules.
- Add unit tests with `pytest`.
- Keep minimal external dependencies unless justified.
- Suggest package metadata and documentation improvements.

## Immediate priorities for contributors

1. Add domain logic to `src/movefit` (e.g., feature modules, services).
2. Add a `tests/` folder and `pytest` coverage.
3. Update `pyproject.toml` with dependencies and optional dev dependencies.

## Guidance for future agent customizations

- If different scopes emerge (CLI, API, ingestion), add specific `*.instructions.md` files under `.github/instructions/` with `applyTo` patterns.
- Add a `.github/hooks/pre-commit` hook to run formatting and static checks.
