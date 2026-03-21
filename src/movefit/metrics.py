from __future__ import annotations

from datetime import datetime
from typing import Generator, List, Tuple


def weight_lb_to_kg(weight_lb: float) -> float:
    """Convert pounds to kilograms."""
    return weight_lb * 0.45359237


def calculate_bmi(
    weight_kg: float,
    height_m: float | None = None,
    height_cm: float | None = None,
) -> float | None:
    """Calculate BMI from weight (kg) and height (m or cm)."""
    if height_m is None and height_cm is None:
        return None
    if height_m is None and height_cm is not None:
        height_m = height_cm / 100.0

    if height_m is None or height_m <= 0:
        return None

    return weight_kg / (height_m * height_m)


def calculate_slopeline(points: List[Tuple[datetime, float]]) -> float:
    """Compute OLS slope for a series of (datetime, value) points."""
    if len(points) < 2:
        return 0.0

    xs = [p[0].timestamp() for p in points]
    ys = [p[1] for p in points]

    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)

    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    return num / den if den != 0 else 0.0
