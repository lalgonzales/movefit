# Movefit Frontend MVP - Getting Started Guide

Objective: Start a minimal React app consuming Movefit API.

## Main steps

1. Switch to `feature/frontend-mvp` branch.

2. Backend (FastAPI):
   - Enable `CORSMiddleware` in `src/movefit/main.py`.
   - Add `GET /healthz` returning `{"status": "ok"}`.
   - Adjust `GET /summary` to return default values when no measurements exist.

3. Tests (`tests/test_measurements_api.py`):
   - Add or assert `test_summary_no_data`. (done)
   - Run `pixi run pytest -q` (done)

4. Documentation: keep `docs/api.md` updated with endpoint contract. (done)

5. Frontend (React):
   - `npm create vite@latest movefit-ui -- --template react` (done via scaffold folder)
   - `npm install`
   - `npm install axios`
   - Implement API client and pages: summary, measurements, trends, goals (done minimal).


## Acceptance criteria

- `GET /summary` returns `total: 0` and no 404 when database has no data.
- `GET /healthz` returns `{"status": "ok"}`.
- Tests pass and docs are up to date.
