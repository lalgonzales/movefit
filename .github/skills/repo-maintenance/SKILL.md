---
name: repo-maintenance
version: 1.0
summary: "Repository synchronization and stale branch cleanup workflow for AI-assisted development."
---

# repo-maintenance Skill

This skill is designed to standardize the baseline repository hygiene flow before new features are developed.

## Intent

- Ensure local branch state is clean
- Fast-forward local main from origin
- Remove merged stale local branches
- Optionally, remove closed remote branches from origin
- Avoid duplicated work by enforcing clean starting conditions

## Inputs

- `current_branch`: str (path-like, current git branch)
- `main_branch`: str (default: `main`)
- `cleanup_remote`: bool (default: true)
- `exclude`: list[str] (branches to keep, e.g. `['main', 'develop']`)

## Output

- `status`: enum [`clean`, `dirty`, `conflict`, `error`]
- `details`: object with keys:
  - `current_branch`
  - `local_main` (bool)
  - `uncommitted_changes` (bool)
  - `forced_pull` (bool)
  - `deleted_local_branches` (list[str])
  - `deleted_remote_branches` (list[str])

## Workflow

1. Check if there are uncommitted changes (`git status --porcelain`).
   - if yes, set `status = dirty` and add instructions to stage/commit/stash.
2. If `current_branch != main_branch`: checkout `main_branch`.
3. `git pull origin main_branch`.
4. Detect merged branches:
   - `git branch --merged main_branch | grep -vE "\*(.*main.*)|\b$(exclude|join|pipe)\b"`
   - delete those local branches.
5. If `cleanup_remote`, query remote branches and match those merged to main on server APIs or `git branch -r --merged` then `git push origin --delete` each stale.
6. Set `status = clean` on success.

## Notes

- This is intended to be called by coordinator or before starting feature-level work.
- If a branch has a pull request open, it may not be safe to delete remote; this skill should include a guard.
