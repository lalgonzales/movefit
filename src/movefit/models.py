from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, SQLModel


class MeasurementBase(SQLModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    device_mac: str
    device_name: Optional[str] = None
    weight_lb: float
    weight_kg: float
    body_fat_pct: Optional[float] = None
    bmi: Optional[float] = None


class Measurement(MeasurementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementRead(MeasurementBase):
    id: int


class MeasurementSummary(SQLModel):
    total: int
    average_weight_kg: float
    min_weight_kg: float
    max_weight_kg: float
    average_bmi: Optional[float]
    average_body_fat_pct: Optional[float]


class TrendPoint(SQLModel):
    timestamp: datetime
    weight_kg: float
    bmi: Optional[float]


class MeasurementTrends(SQLModel):
    metric: str
    points: list[TrendPoint]


class BulkImportResult(SQLModel):
    imported: int
    skipped: int
    errors: List[str]


class MeasurementList(SQLModel):
    measurements: list[MeasurementRead]
