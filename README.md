# Movefit
[![CI](https://github.com/${{ github.repository }}/actions/workflows/ci.yml/badge.svg)](https://github.com/${{ github.repository }}/actions/workflows/ci.yml)

Current project status: fully functional backend with measurement endpoints, analysis APIs, and bulk import (including JSON and XLSX support).

## Branches and flow
- Main branch: `main`
- Feature branch development: `feature/api-pagination`, `feature/xlsx-import`, etc.
- Branch `feature/repo-status` was used to consolidate final state documentation.

## Completed tasks
- Measurement CRUD endpoints
- Bulk import (JSON + XLSX)
- Summary / trends / alerts / goals endpoints
- API pagination and filter support
- Unit tests with `pytest` (passing tests)
- Dependencies and environment managed via `pixi`

## Next steps
1. Add CI workflow in `.github/workflows/ci.yml`.
2. Implement a lightweight frontend for consumption.
3. Publish, document, and version the application.

## Development with pixi
Use `pixi` for dependency and environment management to ensure reproducible builds.
Direct Python invocations are not allowed outside `pixi` control (policy enforcement). Use these exact commands:
- `pixi install`
- `pixi run test` (runs pytest)
- `pixi run python -m pytest -q`
- `pixi run python -m hatchling check`
- `pixi run python -m hatchling build`
- `pixi run pre-commit run --all-files`

> Do not run `python -m pytest` or `python -m hatchling` directly; always run through `pixi run ...` to comply with project policy.
