# Movefit API - Minimal Documentation

Base URL: `http://localhost:8000`

## Endpoints

- `GET /healthz`
  - Response: `200` with `{
  "status": "ok"
}`

- `GET /measurements`
  - Returns a list of measurements.
  - Query parameters: `offset`, `limit`, `from`, `to`, `sort`.

- `POST /measurements`
  - Create a new measurement.

- `POST /measurements/bulk-import`
  - Bulk import measurements from JSON.

- `POST /measurements/bulk-import/xlsx`
  - Import measurements from an XLSX file.

- `GET /summary`
  - Returns aggregates: `total`, `average_weight_kg`, `min_weight_kg`, `max_weight_kg`, etc.

- `GET /trends?metric=weight|bmi`
  - Returns trend points for weight or BMI.

- `GET /alerts`
  - Returns generated alerts based on thresholds.

- `GET /goals`, `POST /goals`
  - List and create goals.
