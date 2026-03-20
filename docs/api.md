# Movefit API Specification

## Overview

API base path: `/`
Auto docs: `/docs`, `/redoc`

Primary entities:
- `Measurement`
- `Goal`
- `Summary`
- `Trend`

## POST /measurements

Create a measurement record.

Request body (JSON):
- `timestamp` (string, ISO-8601, required)
- `device_mac` (string, required)
- `device_name` (string, required)
- `weight_lb` (float, required)
- `body_fat_pct` (float, required)
- `bmi` (float, optional; server can recalc)
- `skeletal_muscle_pct` (float, required)
- `muscle_mass_lb` (float, optional)
- `protein_pct` (float, optional)
- `tdee` (float, optional)
- `lean_mass_lb` (float, optional)
- `subcutaneous_fat_pct` (float, optional)
- `visceral_fat` (float, optional)
- `body_water_pct` (float, optional)
- `bone_mass_lb` (float, optional)
- `body_type` (string, optional)
- `metabolic_age` (int, optional)
- `raw_source` (string, optional)

Response 201:
- `id` (int)
- created resource fields

Example request:
```json
{
  "timestamp": "2026-03-20T08:00:00Z",
  "device_mac": "00:11:22:33:44:55",
  "device_name": "Feelfit Scale",
  "weight_lb": 170.5,
  "body_fat_pct": 18.4,
  "skeletal_muscle_pct": 42.1,
  "muscle_mass_lb": 73.0,
  "protein_pct": 15.2,
  "tdee": 2100,
  "lean_mass_lb": 139.2,
  "subcutaneous_fat_pct": 8.1,
  "visceral_fat": 10.2,
  "body_water_pct": 54.3,
  "bone_mass_lb": 6.7,
  "body_type": "mesomorph",
  "metabolic_age": 29,
  "raw_source": "xls-import-v1"
}
```

## GET /measurements

Query params:
- `offset` (int, default 0)
- `limit` (int, default 100, max 1000)
- `from` (datetime, optional)
- `to` (datetime, optional)

Response 200: list of `Measurement` objects.

## GET /measurements/{id}

Response 200: single Measurement
Response 404: not found

## GET /measurements/latest

Response 200: last Measurement by timestamp.

## GET /summary

Query params:
- `from` (datetime, optional)
- `to` (datetime, optional)

Response 200:
- `count`
- `weight_avg`/`weight_delta`
- `body_fat_avg`/`body_fat_delta`
- `bmi_avg`/`bmi_delta`
- `trend` (enum: improving/stable/regressing)

## GET /trends

Query params:
- `window` (int, default 7)
- `metric` (str, one of `weight`, `body_fat`, `bmi`)

Response 200:
- `points`: list of `{timestamp, value}`
- `slope`
- `category`

## POST /measurements/bulk-import

Accepts JSON array or file upload (TODO):
- each row same fields as `/measurements`.

Response 201:
- `imported` count
- `skipped` count
- `errors` list

## Goals

### POST /goals

Payload:
- `target_weight_lb` (float, required)
- `target_date` (date, required)
- `type` (`weight` | `body_fat`)

Response 201: created goal.

### GET /goals

Response 200: active goals list.
