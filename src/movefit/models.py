from __future__ import annotations

from datetime import date, datetime, timezone
from typing import List, Optional

from sqlmodel import Field, SQLModel


class MeasurementBase(SQLModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    device_mac: str
    device_name: Optional[str] = None
    weight_lb: float
    weight_kg: Optional[float] = None
    body_fat_pct: Optional[float] = None
    bmi: Optional[float] = None


class Measurement(MeasurementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementRead(MeasurementBase):
    id: int


# analytics models
class MeasurementSummary(SQLModel):
    total: int
    average_weight_kg: Optional[float] = None
    min_weight_kg: Optional[float] = None
    max_weight_kg: Optional[float] = None
    average_bmi: Optional[float]
    average_body_fat_pct: Optional[float]


class TrendPoint(SQLModel):
    timestamp: datetime
    value: float


class MeasurementTrends(SQLModel):
    metric: str
    points: List[TrendPoint]
    slope: float
    category: str


class BulkImportResult(SQLModel):
    imported: int
    skipped: int
    errors: List[str]


class AlertItem(SQLModel):
    measurement_id: int
    metric: str
    value: float
    message: str


class AlertList(SQLModel):
    alerts: List[AlertItem]


class GoalBase(SQLModel):
    target_weight_lb: float
    target_date: date
    type: str


class Goal(GoalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    id: int


class MeasurementList(SQLModel):
    measurements: List[MeasurementRead]
