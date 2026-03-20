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
    description="API to ingest and query body composition data.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.post(
    "/measurements",
    response_model=models.MeasurementRead,
    summary="Create a measurement",
    description="Create a single measurement record.",
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
    description="Import multiple measurements in one request.",
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
    description="Get all measurements ordered by timestamp.",
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
    description="Get the latest measurement by timestamp.",
    tags=["measurements"],
)
def read_latest_measurement(session: Session = Depends(db.get_session)):
    statement = select(models.Measurement).order_by(models.Measurement.timestamp.desc()).limit(1)
    measurement = session.exec(statement).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="No measurements found")
    return measurement


@app.get(
    "/measurements/{measurement_id}",
    response_model=models.MeasurementRead,
    summary="Get a measurement",
    description="Get a measurement by ID.",
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
    description="Get aggregated measurement stats.",
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
    description="Get measurement trend points for weight or BMI.",
    tags=["analytics"],
)
def measurement_trends(
    metric: str = Query("weight", pattern="^(weight|bmi)$"),
    session: Session = Depends(db.get_session),
):
    statement = select(models.Measurement).order_by(models.Measurement.timestamp)
    results = session.exec(statement).all()

    points = []
    for m in results:
        value = m.weight_kg if metric == "weight" else (m.bmi or 0.0)
        points.append(models.TrendPoint(timestamp=m.timestamp, value=value))

    # cheap slope estimator
    slope = 0.0
    if len(points) > 1:
        x_vals = list(range(len(points)))
        y_vals = [p.value for p in points]
        mean_x = sum(x_vals) / len(x_vals)
        mean_y = sum(y_vals) / len(y_vals)
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
        den = sum((x - mean_x) ** 2 for x in x_vals)
        slope = num / den if den != 0 else 0.0

    category = "stable"
    if slope > 0.01:
        category = "increasing"
    elif slope < -0.01:
        category = "decreasing"

    return models.MeasurementTrends(metric=metric, points=points, slope=slope, category=category)


@app.get(
    "/alerts",
    response_model=models.AlertList,
    summary="Get health alerts",
    description="Generate alerts based on recent measurements.",
    tags=["analytics"],
)
def get_alerts(session: Session = Depends(db.get_session)):
    measurements = session.exec(select(models.Measurement).order_by(models.Measurement.timestamp)).all()
    alerts: list[models.AlertItem] = []

    for i, m in enumerate(measurements):
        if m.body_fat_pct is not None and m.body_fat_pct > 30.0:
            alerts.append(models.AlertItem(
                measurement_id=m.id,
                metric="body_fat_pct",
                value=m.body_fat_pct,
                message="Body fat percentage above healthy threshold",
            ))

        if m.bmi is not None and m.bmi > 30.0:
            alerts.append(models.AlertItem(
                measurement_id=m.id,
                metric="bmi",
                value=m.bmi,
                message="BMI is in obesity range",
            ))

        if i > 0:
            prev = measurements[i - 1]
            if m.weight_kg - prev.weight_kg > 2.0:
                alerts.append(models.AlertItem(
                    measurement_id=m.id,
                    metric="weight_kg",
                    value=m.weight_kg,
                    message="Rapid weight gain (>2kg since last reading)",
                ))

    return models.AlertList(alerts=alerts)


@app.post(
    "/goals",
    response_model=models.GoalRead,
    status_code=201,
    summary="Create goal",
    description="Set a new weight/body fat goal.",
    tags=["goals"],
)
def create_goal(
    payload: models.GoalCreate,
    session: Session = Depends(db.get_session),
):
    goal = models.Goal.model_validate(payload)
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@app.get(
    "/goals",
    response_model=list[models.GoalRead],
    summary="List goals",
    description="List active goals.",
    tags=["goals"],
)
def read_goals(session: Session = Depends(db.get_session)):
    return session.exec(select(models.Goal)).all()
