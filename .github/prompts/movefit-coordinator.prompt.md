# movefit-coordinator prompt template

Use this prompt when coordinating multi-agent tasks in the movefit repository.

## Inputs
- `goal`: user-facing objective (e.g., implement endpoint, add metric module).
- `scope`: high-level feature scope or boundaries.
- `priority`: if multiple tasks, list in order.

## Template
1. Summarize the requested feature/issue and confirm constraints (platform, Python 3.11, no extra dependencies unless justified).
2. Break into sub-tasks and assign to subagents:
   - `movefit-data` for calculations and core logic.
   - `movefit-db` for persistence schema and migration policy.
   - `movefit-fastapi` for REST API layer (if needed).
   - `movefit-tests` for unit/integration tests.
   - `movefit-ci` for pipeline & quality gates.
3. Define output artifacts and acceptance criteria (files/behavior/tests).
4. Ask user for missing clarification if any.

## Example usage
- "Implement BMI and trend tracking in movefit with API GET endpoint and tests."
- "Coordinate data migration design for new measurement table."
