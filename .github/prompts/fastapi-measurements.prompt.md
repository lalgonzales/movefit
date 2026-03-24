---
description: "Prompt for generating FastAPI endpoints for movefit measurement ingestion and querying."
tools:
  - search
  - execute/runInTerminal
---

Given the Movefit design document, create FastAPI route handlers for the following endpoints:
- `POST /measurements`
- `GET /measurements` with filters `start`, `end`, `device_mac`, `limit`, `offset`
- `GET /measurements/{id}`
- `GET /summary`
- `GET /trends`

Include:
- Pydantic request/response models
- detailed validation
- error handling with HTTP status codes
- comments and docstrings
