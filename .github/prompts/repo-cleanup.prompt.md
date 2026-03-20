# Repo cleanup prompt (for everybody)

You are the project coordinator agent. Before starting any new feature or design task, validate repository hygiene using the `repo-maintenance` skill.

## Task

1. Determine current branch.
2. If not on `main`, switch to `main`.
3. Pull latest main from remote: `git pull origin main`.
4. Identify local merged branches against main, excluding protected branches (`main`, `develop`, `release/*`).
5. Delete merged local branches.
6. Check remote branch list for merged / closed branches and prune with `git push origin --delete` when safe.

## Expected output

- `status`: `clean` / `dirty` / `conflict` / `error`
- `details`: description of operations performed, deleted branches, and actions for unresolved issues.
- do not proceed to feature implementation until `status` is `clean`.

## Scenarios to handle

- On `main` already (skip checkout).
- With uncommitted changes (return `dirty` and avoid automatic cleanup).
- No network (report error with suggestion).
- Already clean (return `clean`).

## Example

```
status: clean
details:
  current_branch: main
  pulled: true
  deleted_local_branches: [feature/api-specs, feature/dependabot]
  deleted_remote_branches: [feature/api-specs, feature/dependabot]
```
