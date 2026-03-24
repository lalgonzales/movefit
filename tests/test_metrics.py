from datetime import datetime, timedelta, timezone

import pytest

from movefit import metrics


def test_weight_lb_to_kg():
    assert metrics.weight_lb_to_kg(0) == 0
    assert metrics.weight_lb_to_kg(2.20462) == pytest.approx(1.0, rel=1e-4)


def test_calculate_bmi_none_height():
    assert metrics.calculate_bmi(70.0) is None


def test_calculate_bmi_height_m():
    assert pytest.approx(
        metrics.calculate_bmi(70.0, height_m=1.75), rel=1e-6
    ) == pytest.approx(22.857142, rel=1e-6)


def test_calculate_bmi_height_cm():
    assert pytest.approx(
        metrics.calculate_bmi(70.0, height_cm=175), rel=1e-6
    ) == pytest.approx(22.857142, rel=1e-6)


def test_calculate_slopeline_linear():
    now = datetime.now(timezone.utc)
    points = [(now + timedelta(days=i), 100.0 + i * 1.5) for i in range(5)]
    slope = metrics.calculate_slopeline(points)
    assert slope > 0


def test_calculate_slopeline_constant():
    now = datetime.now(timezone.utc)
    points = [(now + timedelta(days=i), 50.0) for i in range(3)]
    assert metrics.calculate_slopeline(points) == pytest.approx(0.0)
