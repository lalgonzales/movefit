# movefit-checks skill

This skill provides guidance for pull request check enforcement in movefit projects.

## Purpose
- Check for required CI checks: pytest run, lint (black/isort), and build metadata.
- Suggest the relevant command to run in environment.

## Rules
- Always encourage `pixi task test` and `pixi task build` for pull request readiness.
- If repository has `.github/workflows`, suggest `github action` names from those workflows (e.g., `pytest`, `lint`).
- Validate that new changes include tests for behavior and docs updates for APIs.

## Example steps
1. Run `pixi task test`; expect exit code 0.
2. Run `python -m hatchling build` and `python -m hatchling check`.
3. Run `black --check .` and `isort --check-only .`.
