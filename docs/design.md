# Movefit Design Document

## Overview

- App: FastAPI backend for ingestion/query/analysis of body composition data (weight, fat, muscle, etc.).
- MVP goal: measurement ingestion + timeline + metric summary + goals.
- Initial input: Excel dump with scale readings (`Índice_físico-Feelfit...`).

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
- POST /measurements/bulk-import
- GET /measurements
- GET /measurements/{id}
- GET /measurements/latest
- GET /summary
- GET /trends
- GET /alerts
- POST /goals
- GET /goals

## Persistence

MVP: SQLite + SQLModel/SQLAlchemy.

## Proposed folder structure

- `src/movefit/` - code
- `tests/` - unit tests
- `docs/design.md` - this document
- `data/raw/` - original XLSX files (versioned as needed; usually `.gitignore`)
- `data/processed/` - CSV/JSON export from import process

## Excel data flow proposal

1. Store original XLSX files in `data/raw/` (dev only). Example: `data/raw/Indice_fisico-2026...xlsx`.
2. Track versions in `README` or `data/README.md`:
   - date
   - source
   - cleanup notes
3. In CI/production, manage via `POST /measurements/bulk-import` endpoint and/or script `scripts/import_xlsx.py`.
4. Do not commit large raw data files into the main repository in production. Use dedicated storage (S3, Google Drive, etc.) and version-only metadata.

## Roadmap (simple to complex)

1. Model + API CRUD + tests.
2. Excel import.
3. Summary / trends / derived calculations.
4. Goals / alerts / multi-tenant.
5. JWT auth, ML, frontend.

## Agent orchestration and Git operations

- `movefit-coordinator` orquesta (subagentes: `movefit-fastapi`, `movefit-data`, `movefit-db`, `movefit-tests`, `movefit-ci`, `movefit-docs`, `movefit-git`).
- `movefit-ci` gestiona la canalización de CI/CD y delega operaciones de repositorio a `movefit-git`.
- `movefit-git` ejecuta `git status`, `git add`, `git commit`, `git push`, `git tag`, `git log` usando `execute/runInTerminal`.
- Se recomienda evitar fuerza-push automáticos y reescritura de historial en flujos de CI.

## Design license

This design is the primary blueprint for `movefit`; update with changes in `docs/design.md`.
