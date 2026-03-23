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
- `body` strongly recommended for all non-trivial commits, with:
  - what changed
  - why it changed
  - impact/side effects (if any)
  - test instructions (if applicable)
- `footer` strongly recommended for references and releasability info:
  - `Closes #<issue>`
  - `BREAKING CHANGE: ...`
  - `Co-authored-by: ...`
- Prefer `git add -p` or `git add <files>`; avoid `git add .`.

Example:
```txt
feat(measurement): add csv bulk import endpoint

Implement POST /measurements/bulk-import with row validation.
- support multiple rows
- report parse errors with row-context
- skip empty lines and trim whitespace

Add `tests/test_measurements_api.py::test_bulk_import_success`.

Closes #43
```
