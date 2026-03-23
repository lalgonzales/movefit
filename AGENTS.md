# Movefit Custom Agent Definitions

This file documents project agents and how to use them.

## Agenda

- `movefit-coordinator`: high-level coordinator agent.
- `movefit-fastapi`: agent for API design/implementation (FastAPI + Pydantic + SQLModel).
- `movefit-data`: agent for calculations and metrics.
- `movefit-db`: agent for schema and persistence.
- `movefit-tests`: agent for unit and integration testing.
- `movefit-ci`: agent for CI pipeline and pre-commit.
- `movefit-git`: agent for git operations (commit/tag/push) from CI/coordinator workflows.
- `movefit-docs`: agent for documentation and design maintenance.

## Recommended usage

1. Start with `movefit-coordinator` to define feature strategy.
2. Use specialized subagents for each stage.
3. Validate output with `movefit-tests` and `movefit-ci`.
4. Update `docs/design.md` via `movefit-docs`.

## Recommended minimal agent set

- `movefit-coordinator` (required): orchestration point.
- `movefit-tests` (required): test and regression validation.
- `movefit-ci` (required): CI pipeline checks and lint enforcement.
- `movefit-git` (optional): workflow automation for commit/push.
- `movefit-data`, `movefit-db`, `movefit-fastapi`, `movefit-docs`, `movefit-frontend` (keep only when a clear team ownership or process need exists).

## When to prune

- If an agent file is no longer referenced in active workflows, remove it and keep an audit in a single changelog section (e.g., `docs/agent-cleanup.md`).
- Prioritize reducing duplication in `copilot-instructions.md` and `agent-customization.instructions.md`.

## Agent metadata and standardization

- Each agent has a definition in `.github/agents/<agent>.agent.md` with YAML frontmatter.
- `tools:` should be limited to role-required capabilities (principle of least privilege).
- `user-invocable:` is set to `true` only for the coordinator and optionally manual development agents.
- Recent changes: tool permissions are adjusted per agent responsibility, and `movefit-git` is not invocable directly by a user (from coordinator/CI).
- `movefit-git` uses explicit staging and Conventional Commits style.
- Keep `docs/design.md` updated with agent orchestration and expected workflow.

### Pixi policy
- This is a pixi managed project. Use `pixi` for all dependency and environment management to ensure reproducibility.
- Avoid manual `pip` installs outside of `pixi` commands.

## Commit splitting policy
- At least one commit per logical category: docs, code, tests, tooling.
- Do not combine docs and feature code in a single commit.
- Prefer granular commits to ease review and rollback.
- Use Conventional Commits with detailed body and footer for each commit:
  - body: background + what/why/how + test steps
  - footer: issue references / `BREAKING CHANGE` / co-author info
- Avoid one-line/bare subjects like `update(docs): xyz` without context.
