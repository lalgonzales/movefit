from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .models import MeasurementCreate


def read_xlsx_measurements(xlsx_path: str | Path, error_log: list[str] | None = None) -> Iterable[MeasurementCreate]:
    df = pd.read_excel(xlsx_path, sheet_name=0)

    # Mapping for internal API fields already in DB model
    field_map = {
        'timestamp': 'timestamp',
        'device_mac': 'device_mac',
        'device_name': 'device_name',
        'weight_lb': 'weight_lb',
        'weight_kg': 'weight_kg',
        'body_fat_pct': 'body_fat_pct',
        'bmi': 'bmi',
        'skeletal_muscle_pct': 'skeletal_muscle_pct',
        'muscle_mass_lb': 'muscle_mass_lb',
        'protein_pct': 'protein_pct',
        'tdee': 'tdee',
        'lean_mass_lb': 'lean_mass_lb',
        'subcutaneous_fat_pct': 'subcutaneous_fat_pct',
        'visceral_fat': 'visceral_fat',
        'body_water_pct': 'body_water_pct',
        'bone_mass_lb': 'bone_mass_lb',
        'body_type': 'body_type',
        'metabolic_age': 'metabolic_age',
        'raw_source': 'raw_source',
    }

    header_alias_map = {
        'measurement time': 'timestamp',
        'tiempo de medición': 'timestamp',
        'weight(lb)': 'weight_lb',
        'peso(lb)': 'weight_lb',
        'body fat(%)': 'body_fat_pct',
        'grasa corporal(%)': 'body_fat_pct',
        'lean weight(lb)': 'lean_mass_lb',
        'peso magro(lb)': 'lean_mass_lb',
        'visceral fat': 'visceral_fat',
        'grasa visceral': 'visceral_fat',
        'device mac': 'device_mac',
        'mac dispositivo': 'device_mac',
        'device name': 'device_name',
        'nombre dispositivo': 'device_name',
    }

    def normalize_header(name: str) -> str:
        return str(name).strip().lower()

    column_mapping: dict[str, str] = {}
    for col in df.columns:
        normalized = normalize_header(col)
        if normalized in header_alias_map:
            column_mapping[col] = header_alias_map[normalized]
        elif normalized in field_map:
            column_mapping[col] = field_map[normalized]

    # Keep raw column names that are already internal fields.
    for internal in field_map:
        if internal in df.columns and internal not in column_mapping:
            column_mapping[internal] = field_map[internal]

    for idx, row in enumerate(df.iterrows()):
        _, row = row
        payload = {}
        for col, attr in column_mapping.items():
            if col in row and pd.notna(row[col]):
                payload[attr] = row[col]

        try:
            yield MeasurementCreate(**payload)
        except Exception as exc:
            message = f"row[{idx}] parse error: {exc}"
            if error_log is not None:
                error_log.append(message)
            else:
                raise

