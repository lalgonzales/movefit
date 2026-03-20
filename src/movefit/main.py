from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select, func

from . import db, models


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield


app = FastAPI(
    title="movefit",
    description="API to ingest and query body composition measurements.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post(
    "/measurements",
    response_model=models.MeasurementRead,
    summary="Create a measurement",
    description="Add a new measurement entry with weight, body fat, BMI and metadata.",
    tags=["measurements"],
)
def create_measurement(
    payload: models.MeasurementCreate,
    session: Session = Depends(db.get_session),
):
    model = models.Measurement.model_validate(payload)

    if not model.weight_kg and model.weight_lb:
        model.weight_kg = model.weight_lb * 0.45359237

    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@app.post(
    "/measurements/bulk-import",
    response_model=models.BulkImportResult,
    status_code=201,
    summary="Bulk import measurements",
    description="Import multiple measurement rows in a single request.",
    tags=["measurements"],
)
def bulk_import_measurements(
    payload: list[dict[str, Any]],
    session: Session = Depends(db.get_session),
):
    imported = 0
    skipped = 0
    errors: list[str] = []

    for idx, row in enumerate(payload):
        try:
            measurement = models.MeasurementCreate.model_validate(row)
            if not measurement.weight_kg and measurement.weight_lb:
                measurement.weight_kg = measurement.weight_lb * 0.45359237

            db_model = models.Measurement.model_validate(measurement)
            session.add(db_model)
            imported += 1
        except Exception as exc:
            skipped += 1
            errors.append(f"row[{idx}]: {exc}")

    session.commit()

    return models.BulkImportResult(imported=imported, skipped=skipped, errors=errors)


@app.get(
    "/measurements",
    response_model=list[models.MeasurementRead],
    summary="List measurements",
    description="Retrieve all recorded measurements in timestamp order.",
    tags=["measurements"],
)
def read_measurements(session: Session = Depends(db.get_session)):
    statement = select(models.Measurement).order_by(models.Measurement.timestamp)
    results = session.exec(statement).all()
    return results


@app.get(
    "/measurements/latest",
    response_model=models.MeasurementRead,
    summary="Latest measurement",
    description="Get the most recent measurement by timestamp.",
    tags=["measurements"],
)
def read_latest_measurement(session: Session = Depends(db.get_session)):
    statement = select(models.Measurement).order_by(models.Measurement.timestamp.desc()).limit(1)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="No measurements found")
    return result


@app.get(
    "/measurements/{measurement_id}",
    response_model=models.MeasurementRead,
    summary="Get a measurement",
    description="Retrieve one measurement by its numeric ID.",
    tags=["measurements"],
)
def read_measurement(measurement_id: int, session: Session = Depends(db.get_session)):
    measurement = session.get(models.Measurement, measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement


@app.get(
    "/summary",
    response_model=models.MeasurementSummary,
    summary="Measurement summary",
    description="Return aggregate statistics for measurements.",
    tags=["analytics"],
)
def measurement_summary(session: Session = Depends(db.get_session)):
    statement = select(
        func.count(models.Measurement.id),
        func.avg(models.Measurement.weight_kg),
        func.min(models.Measurement.weight_kg),
        func.max(models.Measurement.weight_kg),
        func.avg(models.Measurement.bmi),
        func.avg(models.Measurement.body_fat_pct),
    )
    row = session.exec(statement).one()
    if row[0] == 0:
        raise HTTPException(status_code=404, detail="No measurements available")

    return models.MeasurementSummary(
        total=row[0],
        average_weight_kg=float(row[1]) if row[1] is not None else 0.0,
        min_weight_kg=float(row[2]),
        max_weight_kg=float(row[3]),
        average_bmi=float(row[4]) if row[4] is not None else None,
        average_body_fat_pct=float(row[5]) if row[5] is not None else None,
    )


@app.get(
    "/trends",
    response_model=models.MeasurementTrends,
    summary="Measurement trends",
    description="Return a time series for weight and BMI.",
    tags=["analytics"],
)
def measurement_trends(
    metric: str = Query("weight", pattern="^(weight|bmi)$"),
    session: Session = Depends(db.get_session),
):
    if metric not in {"weight", "bmi"}:
        raise HTTPException(status_code=400, detail="Invalid metric")

    statement = select(models.Measurement).order_by(models.Measurement.timestamp)
    results = session.exec(statement).all()

    points = [
        models.TrendPoint(timestamp=m.timestamp, weight_kg=m.weight_kg, bmi=m.bmi)
        for m in results
    ]

    return models.MeasurementTrends(metric=metric, points=points)
