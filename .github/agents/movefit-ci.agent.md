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

## Focus

- `.github/workflows/python-app.yml`
  - install deps
  - pytest
  - `ruff check` or `flake8`, `ruff format` / `black`
  - `python -m hatchling check`
- `.pre-commit-config.yaml` setup- Git operations para CI release flow (commit, tag, push) usando `execute/runInTerminal`
## Deliverables

- build status badge for README
- quality gates for PRs

## Handoff

When passing, prompt `movefit-docs` for release notes and changelog updates.
