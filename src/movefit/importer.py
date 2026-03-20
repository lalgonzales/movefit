from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .models import MeasurementCreate


def read_xlsx_measurements(xlsx_path: str | Path) -> Iterable[MeasurementCreate]:
    df = pd.read_excel(xlsx_path, sheet_name=0)

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

    for _, row in df.iterrows():
        payload = {}
        for col, attr in field_map.items():
            if col in row and pd.notna(row[col]):
                payload[attr] = row[col]

        try:
            yield MeasurementCreate(**payload)
        except Exception:
            continue
