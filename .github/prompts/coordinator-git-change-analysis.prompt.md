# prompt: coordinator-git-change-analysis

## Objective
Help the `movefit-coordinator` agent analyze the current branch/PR state and, together with `movefit-git`, decide which other agents should act based on real change types (code, business logic, tests, CI, docs, permissions, prompts/agents metadata).

## Expected flow
1. Run `movefit-git` to collect:
   - `git status --short`
   - `git diff --name-only main..HEAD`
   - `git log --oneline --decorate --graph -n 10`
2. Classify changed files by area:
   - `src/movefit/**` → code/business logic
   - `tests/**` → coverage/regression
   - `.github/workflows/**`, `tool.pixi` → CI
   - `.github/agents/**`, `.github/prompts/**`, `.github/instructions/**` → coordination/agent metadata
   - others (docs, infra, etc.)
3. For each area, infer requirements:
   - tests needed/missing
   - case review, data quality, invariants
   - workflow adjustments, pixi command, CI matrix
   - prompt/agent contract fixes
4. Recommend agents and actions:
   - `movefit-data`: metrics, calculations, business rules
   - `movefit-fastapi`: endpoints, validation, contracts
   - `movefit-db`: model/persistence
   - `movefit-tests`: add/extend tests
   - `movefit-ci`: workflow, badge, lint
   - `movefit-docs`: API documentation/release notes
   - `movefit-git`: commit/branch/PR messaging
5. Generate a structured work plan (priorities + exact commands).
6. If the change basis is unclear, ask the user: "which business feature are we trying to deliver?" and/or "please provide issue/project context.".

## Output style
- Very concise, step-by-step.
- Always indicate why and what is being validated.
- The coordinator must never execute shell/git commands itself; only recommend actions and invoke other agents (e.g., `movefit-git` for git operations).
- Ensure nothing is executed until explicit confirmation.
- Include status tag: `analysis`, `ready-to-execute`, `needs-user-input`.

## Invocation example
```text
You are movefit-coordinator. Review branch changes with movefit-git and organize a plan for movefit-data, movefit-fastapi, movefit-tests, and movefit-ci. Prioritize business logic and do not execute anything without confirmation.
```

## Expected result
- Text containing:
  1. Change summary.
  2. Categorization by area.
  3. Tests/CI/git requirements.
  4. Agent list and tasks.
  5. Validation commands to execute.
  6. One clarification question if context is missing.
