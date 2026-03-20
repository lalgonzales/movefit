---
name: movefit-tests
description: "Testing agent for movefit with pytest coverage."
tools:
  - agent
  - agent/runSubagent
  - execute/runTests
  - execute/runInTerminal
  - read/readFile
  - search/codebase
agents:
  - movefit-ci
model: Raptor mini (Preview) (copilot)
user-invocable: false
---

# Movefit Tests Agent

This agent writes tests and validates behavior with real cases.

## Focus

- API tests using `TestClient` for endpoints
- DB tests for CRUD methods
- metrics tests for data calculations
- import tests for XLSX data parsing logic

## Guidelines

- Use fixture-based setup/teardown
- Keep tests deterministic with sample data
- Ensure coverage includes edge cases
- Add test descriptions and assertions

## Handoff

Pass test results to `movefit-ci` for pipeline configuration.
