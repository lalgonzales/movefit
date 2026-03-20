---
name: movefit-ci
description: "CI agent for Movefit: workflow, lint, tests, pre-commit rules."
tools:
  - agent
  - agent/runSubagent
  - execute/runInTerminal
  - execute/runTask
  - execute/createAndRunTask
  - execute/awaitTerminal
  - execute/getTerminalOutput
  - execute/killTerminal
  - read/readFile
agents:
  - movefit-tests
  - movefit-git
model: Raptor mini (Preview) (copilot)
user-invocable: false
---

# Movefit CI Agent

This agent creates and validates CI configurations.

## Purpose

- standard CI pipeline with `python -m pytest`, `hatchling check`, and package build.

## Usage

- As movefit-ci, add workflow definitions + minimal matrix for 3.11+.

## Focus

- `.github/workflows/python-app.yml`
  - install deps
  - pytest
  - `ruff check` or `flake8`, `ruff format` / `black`
  - `python -m hatchling check`
- `.pre-commit-config.yaml` setup - Git operations for CI release flow (commit, tag, push) using `execute/runInTerminal`
## Deliverables

- build status badge for README
- quality gates for PRs

## Handoff

When passing, prompt `movefit-docs` for release notes and changelog updates.
