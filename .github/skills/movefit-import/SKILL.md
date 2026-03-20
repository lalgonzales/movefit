---
name: movefit-import
description: "Import measurements from an Excel workbook into Movefit's data model."
argument-hint: "[xlsx-file-path]"
user-invocable: true
---

# Movefit Import Skill

This skill parses XLSX data and produces normalized records for the `Measurement` model.

## Steps

1. Read the workbook and sheet (default `Sheet1`).
2. Map columns:
   - `Measurement time` -> `timestamp`
   - `Weight(lb)` -> `weight_lb`
   - `Body fat(%)` -> `body_fat_pct`
   - ...
3. Normalize units (lb -> kg, % -> fraction optional).
4. Validate ranges and required fields.
5. Detect duplicates by timestamp + device_id.
6. Emit list of records or save via repository.

## Example command

`/movefit-import data/raw/Indice_fisico-20260318150059.xlsx`


## Source column aliasing
- Support both English and Spanish source headers to avoid parser mismatch:
  - `Measurement time` / `Tiempo de medición` -> `timestamp`
  - `Weight(lb)` / `Peso(lb)` -> `weight_lb`
  - `Body fat(%)` / `Grasa corporal(%)` -> `body_fat_pct`
  - `Lean Weight(lb)` / `Peso magro(lb)` -> `lean_mass_lb`

## References

- `.github/agents/movefit-data.agent.md`
- `docs/design.md`
