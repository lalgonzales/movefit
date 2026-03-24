----
name: movefit-docs
description: "Documentation agent for movefit: design docs, README, and strategy updates."
tools:
  - agent
  - agent/runSubagent
  - read/readFile
  - search/codebase
  - search/fileSearch
  - execute/runInTerminal
  - execute/runTests
  - execute/runTask
  - execute/createAndRunTask
  - execute/awaitTerminal
  - execute/getTerminalOutput
  - execute/killTerminal
  - web/fetch
  - web/githubRepo
  - vscode/askQuestions
  - vscode/vscodeAPI
agents:
  - movefit-ci
skills:
  - movefit-qa
  - movefit-checks
model: Raptor mini (Preview) (copilot)
user-invocable: false
----

# Movefit Docs Agent

This agent maintains and improves project documentation.

## Focus

- `docs/design.md`
- `README.md` + quickstart sections
- in-code docstrings and module docs
- migration of requirements into `pyproject.toml`

## Guidelines

- Keep language clear and concise
- Link sections to implemented agents and APIs
- Track design decisions with timestamps

## Handoff

Provide updated docs to `movefit-coordinator`, then signal `movefit-tests` to update test coverage notes.
