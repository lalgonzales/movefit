# Cleanup to Main Prompt

## Purpose
When the user asks to reset local Git state to a clean `main` branch and prepare for next work, provide precise steps for the agent to perform.

## Input Format
- `user_instruction`: natural-language request.
- `context`: optional, current branch status and any open PR.

## Output Format (Markdown)
1. `Interpretation`: concise summary of intent.
2. `Plan`: ordered commands and checks to execute.
3. `Result`: expected final state.

## Example Invocation
```
/user_instruction "Switch to main, pull latest, delete local feature branches, prune remotes"
/context "current branch feature/frontend-team, PR #17 open"
```

## Implementation Guidance
- Always confirm the current branch before switching.
- Run `git fetch --prune` first.
- Use `git checkout main`, then `git pull`.
- Cleanup local branches hidden by `git branch --merged main` except main.
- Run `git remote prune origin`.
- Report success state: on main, up to date, no local stale branches.
