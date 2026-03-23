# movefit-data prompt template

Use this prompt when defining metric calculation features and analytic behavior.

## Inputs
- `metric`: desired metric name (e.g., BMI, body-fat trend).
- `inputs`: input data model (weights, timestamps, height, age, sex, etc.).
- `output`: desired output schema (value, status, confidence, recommendation).
- `constraints`: performance and dependency constraints (pure python, no heavy libs).

## Template
1. Describe the use case and domain intent clearly.
2. Specify input validation rules and error conditions.
3. Enumerate output fields with types and units.
4. Ask for test cases including edge-case coverage.
5. Mention integration points with `movefit-fastapi` and `movefit-db`.
