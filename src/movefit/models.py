from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

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


class MeasurementList(SQLModel):
    measurements: list[MeasurementRead]
