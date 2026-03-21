# Movefit Design Document

## Overview

- App: FastAPI backend for ingesting/querying/analyzing body composition data (weight, fat, muscle, etc.).
- MVP goal: measurement ingestion + timeline + metric summary + goals.
- Initial input: Excel dump with scale readings (`Physical_Index-Feelfit...`).

## Initial dataset (sheet1)

Captured key columns:
- Measurement time (datetime, `dd/mm/YYYY HH:MM:SS`)
- Weight(lb)
- Body Fat(%)
- BMI
- Skeletal Muscle(%)
- Muscle Mass(lb)
- Muscle Storage Grade
- Protein(%)
- TMB(kcal)
- Lean Weight(lb)
- Subcutaneous Fat Index(%)
- Visceral Fat
- Body Water(%)
- Bone Mass(lb)
- Body Type
- Metabolic Age
- Device MAC Address
- Device Name

### Source header aliasing
- Map raw headers in both English and Spanish to standard fields to avoid ingestion errors.
  - `Measurement time` / `Tiempo de medición` -> `timestamp`
  - `Weight(lb)` / `Peso(lb)` -> `weight_lb`
  - `Body Fat(%)` / `Grasa corporal(%)` -> `body_fat_pct`
  - `Lean Weight(lb)` / `Peso magro(lb)` -> `lean_mass_lb`
  - `Visceral Fat` / `Grasa visceral` -> `visceral_fat`

## Main models

### Measurement
- id
- timestamp
- device_mac
- device_name
- weight_lb
- weight_kg (derived)
- body_fat_pct
- bmi
- skeletal_muscle_pct
- muscle_mass_lb
- muscle_storage_grade
- protein_pct
- tdee
- lean_mass_lb
- subcutaneous_fat_pct
- visceral_fat
- body_water_pct
- bone_mass_lb
- body_type
- metabolic_age
- raw_source

## Planned endpoints

- POST /measurements
- POST /measurements/bulk-import (implemented JSON bulk import; XLSX parser planned)
- GET /alerts (implemented)
- POST /goals (implemented)
- GET /goals (implemented)
- GET /measurements
- GET /measurements/{id}
- GET /measurements/latest
- GET /summary (implemented, range filter pending)
- GET /trends (implemented, window param pending)

## Persistence

MVP: SQLite + SQLModel/SQLAlchemy.

## Proposed folder structure

- `src/movefit/` - code
- `tests/` - unit tests
- `docs/design.md` - this document
- `data/raw/` - original XLSX files (versioned as needed; usually `.gitignore`)
- `data/processed/` - CSV/JSON export from the import process

## Excel data flow proposal

1. Store original XLSX files in `data/raw/` (dev only). Example: `data/raw/Physical_Index-2026...xlsx`.
2. Track versions in `README` or `data/README.md`:
   - date
   - source
   - cleanup notes
3. In CI/production use `POST /measurements/bulk-import` and/or script `scripts/import_xlsx.py`.
4. Do not commit large raw data files in main repository in production. Use dedicated storage (S3, Google Drive, etc.) and version only metadata.

## Roadmap (simple to complex)

1. Model + API CRUD + tests.
2. Excel import.
3. Summary / trends / derived calculations.
4. Goals / alerts / multi-tenant.
5. JWT auth, ML, frontend.

## Agent orchestration and Git operations

- `movefit-coordinator` orchestrates subagents: `movefit-fastapi`, `movefit-data`, `movefit-db`, `movefit-tests`, `movefit-ci`, `movefit-docs`, `movefit-git`.
- `movefit-ci` manages CI/CD pipeline and delegates repository ops to `movefit-git`.
- `movefit-git` executes `git status`, `git add`, `git commit`, `git push`, `git tag`, `git log` via terminal.
- Avoid force push and history rewrite in CI workflows.

## Design license

This design is the primary blueprint for `movefit`; update it in `docs/design.md` for changes.

## Frontend docs

- New folder: `docs/frontend-react-vite-tailwind/`
- Guides: overview, starter-checklist, integration.

## Frontend tooling

- Added VSCode guide in `docs/frontend-react-vite-tailwind/vscode.md`.
- Added skill `.github/skills/movefit-frontend/SKILL.md` and prompt `.github/prompts/frontend-vite-tailwind.prompt.md`.

## Frontend Tooling & Agents

- Added guide files and agent references for React/Vite/Tailwind.
- Added movefit-frontend agent + skill + prompt.
