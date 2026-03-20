# Commit Message Guidelines (Conventional Commits)

To keep Copilot and CI workflows readable and traceable, we follow Conventional Commits:

Format:
```txt
<type>(<scope>): <subject>

<body>

<footer>
```

Common types:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting/code style changes without behavior
- refactor: code restructure without new behavior
- perf: performance improvements
- test: add/update tests
- chore: maintenance tasks

Rules:
- `subject` in present tense, imperative mood, max 72 chars.
- `body` optional, with context and details.
- `footer` for issue references or BREAKING CHANGE.
- Prefer `git add -p` or `git add <files>`; avoid `git add .`.

Example:
```txt
feat(measurement): add csv bulk import endpoint

Implement POST /measurements/bulk-import with row validation.

Closes #43
```
