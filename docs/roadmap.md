# Roadmap

## Current milestone: API and data layer bootstrapping

1. Core API spec (done in docs/api.md)
2. Base models and schemas:
   - `Measurement`, `Goal`, `Summary` (SQLModel)
   - `MeasurementCreate`, `MeasurementRead`, `GoalCreate`, etc.
3. Database setup and session dependency (SQLModel + SQLite local + easy to switch to PostgreSQL)
4. FastAPI routes for CRUD and reporting as in API spec
5. Unit tests for data calculations + API tests with `TestClient`
6. CI pipeline (pytest + hatchling + pre-commit)

## Next features (prioritized)

- Bulk import endpoint for Excel/CSV:
  - parse Excel and detect invalid rows
  - no duplicate insertion (device_mac+timestamp unique key)
- Goals tracking and projection:
  - `GET /goals` current status
  - progress and ETA (linear trend)
- Alerts:
  - thresholds for body fat and weight changes
  - `GET /alerts`, `POST /alerts` for user-defined rules
- Trends engine:
  - 7-day, 30-day rolling averages
  - slope generation (Regression) and category classification
  - cached periodic recomputation to avoid heavy aggregation on every call
- User profiles and devices:
  - multi-tenant support
  - auth (OAuth2/JWT)

## Future expansion

- Manager dashboard (frontend) with charts
- Predictive analytics (ML) with weight + fat trajectories
- Data export (CSV/JSON) and inbound sync integration
- Hosted deployment docs (FastAPI Cloud, Docker, Kubernetes)
