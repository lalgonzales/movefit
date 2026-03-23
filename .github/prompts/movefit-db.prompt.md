# movefit-db prompt template

Use this prompt when defining database schema, ORM models, and migration behavior for Movefit.

## Inputs
- `schema_change`: description of new table/column/relationship.
- `fields`: field names with types and constraints (e.g., `weight_kg: float`, `timestamp: datetime`).
- `migrations`: whether a migration script is required and strategy (e.g., simple add nullable column).

## Template
1. Summarize the intent (e.g., store biometric readings with BMI, fat percentage, metadata).
2. Specify model definitions in `src/movefit/models.py` and/or `src/movefit/schemas.py`.
3. Declare DB-side invariants (not null, unique keys) and indexing for query paths.
4. If using SQLModel, include `Field` metadata for defaults and constraints.
5. Add a mention of data migration strategy and fallback for missing existing rows.
6. Provide test coverage plan for CRUD, schema validation, and edge cases.
