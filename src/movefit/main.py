from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import pandas as pd
from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func

from . import db, importer, metrics, models


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", summary="Health check", tags=["health"])
def healthz():
    return {"status": "ok"}


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
        model.weight_kg = metrics.weight_lb_to_kg(model.weight_lb)

    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@app.get(
    "/measurements",
    response_model=list[models.MeasurementRead],
    summary="List measurements",
    description="Retrieve measurements with pagination and optional time filtering.",
    tags=["measurements"],
)
def read_measurements(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    from_ts: datetime | None = Query(None, alias="from"),
    to_ts: datetime | None = Query(None, alias="to"),
    sort: str = Query("asc", pattern="^(asc|desc)$"),
    session: Session = Depends(db.get_session),
):
    statement = select(models.Measurement)
    if from_ts:
        statement = statement.where(models.Measurement.timestamp >= from_ts)
    if to_ts:
        statement = statement.where(models.Measurement.timestamp <= to_ts)

    statement = statement.order_by(
        models.Measurement.timestamp.asc()
        if sort == "asc"
        else models.Measurement.timestamp.desc()
    )
    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()


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
            if (
                measurement.weight_kg is None or measurement.weight_kg == 0
            ) and measurement.weight_lb:
                measurement.weight_kg = metrics.weight_lb_to_kg(measurement.weight_lb)

            db_model = models.Measurement.model_validate(measurement)
            session.add(db_model)
            imported += 1
        except Exception as exc:
            skipped += 1
            errors.append(f"row[{idx}]: {exc}")

    session.commit()

    return models.BulkImportResult(imported=imported, skipped=skipped, errors=errors)


@app.post(
    "/measurements/bulk-import/xlsx",
    response_model=models.BulkImportResult,
    status_code=201,
    summary="Bulk import measurements from XLSX",
    description="Upload an XLSX file and import measurements from it.",
    tags=["measurements"],
)
def bulk_import_measurements_xlsx(
    file: UploadFile = File(...),
    session: Session = Depends(db.get_session),
):
    imported = 0
    skipped = 0
    errors: list[str] = []

    with NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        contents = file.file.read()
        tmp.write(contents)
        tmp_path = Path(tmp.name)

    try:
        for idx, measurement in enumerate(
            importer.read_xlsx_measurements(tmp_path, error_log=errors)
        ):
            try:
                if (
                    measurement.weight_kg is None or measurement.weight_kg == 0
                ) and measurement.weight_lb:
                    measurement.weight_kg = metrics.weight_lb_to_kg(
                        measurement.weight_lb
                    )

                db_model = models.Measurement.model_validate(measurement)
                session.add(db_model)
                imported += 1
            except Exception as exc:
                skipped += 1
                errors.append(f"row[{idx}]: {exc}")

        session.commit()

    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass

    return models.BulkImportResult(imported=imported, skipped=skipped, errors=errors)


# ... rest of endpoints remain unchanged ...


@app.get(
    "/measurements/latest",
    response_model=models.MeasurementRead,
    summary="Latest measurement",
    description="Get the most recent measurement by timestamp.",
    tags=["measurements"],
)
def read_latest_measurement(session: Session = Depends(db.get_session)):
    statement = (
        select(models.Measurement)
        .order_by(models.Measurement.timestamp.desc())
        .limit(1)
    )
    measurement = session.exec(statement).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="No measurements found")
    return measurement


@app.get(
    "/measurements/{measurement_id}",
    response_model=models.MeasurementRead,
    summary="Get a measurement",
    description="Retrieve a measurement by ID.",
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
    description="Return aggregate stats across measurements.",
    tags=["analytics"],
)
def measurement_summary(
    from_ts: datetime | None = Query(None, alias="from"),
    to_ts: datetime | None = Query(None, alias="to"),
    session: Session = Depends(db.get_session),
):
    statement = select(
        func.count(models.Measurement.id),
        func.avg(models.Measurement.weight_kg),
        func.min(models.Measurement.weight_kg),
        func.max(models.Measurement.weight_kg),
        func.avg(models.Measurement.bmi),
        func.avg(models.Measurement.body_fat_pct),
    )
    if from_ts:
        statement = statement.where(models.Measurement.timestamp >= from_ts)
    if to_ts:
        statement = statement.where(models.Measurement.timestamp <= to_ts)
    row = session.exec(statement).one()
    if row[0] == 0:
        return models.MeasurementSummary(
            total=0,
            average_weight_kg=0.0,
            min_weight_kg=0.0,
            max_weight_kg=0.0,
            average_bmi=None,
            average_body_fat_pct=None,
        )

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
    description="Return a time series for weight/BMI.",
    tags=["analytics"],
)
def measurement_trends(
    metric: str = Query("weight", pattern="^(weight|bmi)$"),
    window: str | None = Query(None, pattern="^(daily|weekly|monthly)$"),
    from_ts: datetime | None = Query(None, alias="from"),
    to_ts: datetime | None = Query(None, alias="to"),
    session: Session = Depends(db.get_session),
):
    statement = select(models.Measurement)
    if from_ts:
        statement = statement.where(models.Measurement.timestamp >= from_ts)
    if to_ts:
        statement = statement.where(models.Measurement.timestamp <= to_ts)
    statement = statement.order_by(models.Measurement.timestamp)
    results = session.exec(statement).all()

    def to_period_start(ts: datetime, window_name: str) -> datetime:
        if window_name == "daily":
            return datetime(ts.year, ts.month, ts.day, tzinfo=ts.tzinfo)
        if window_name == "weekly":
            isoyear, week, _ = ts.isocalendar()
            week_start = date.fromisocalendar(isoyear, week, 1)
            return datetime(
                week_start.year, week_start.month, week_start.day, tzinfo=ts.tzinfo
            )
        if window_name == "monthly":
            return datetime(ts.year, ts.month, 1, tzinfo=ts.tzinfo)
        return ts

    if window is not None:
        by_period: dict[datetime, list[float]] = {}
        for m in results:
            value = m.weight_kg if metric == "weight" else (m.bmi or 0.0)
            period = to_period_start(m.timestamp, window)
            by_period.setdefault(period, []).append(value)

        points = [
            models.TrendPoint(timestamp=period, value=sum(vals) / len(vals))
            for period, vals in sorted(by_period.items())
        ]
    else:
        points = [
            models.TrendPoint(
                timestamp=m.timestamp,
                value=(m.weight_kg if metric == "weight" else (m.bmi or 0.0)),
            )
            for m in results
        ]

    slope = 0.0
    if len(points) > 1:
        slope = metrics.calculate_slopeline([(p.timestamp, p.value) for p in points])

    category = "stable"
    if slope > 0.01:
        category = "increasing"
    elif slope < -0.01:
        category = "decreasing"

    delta = None
    pct_change = None
    trend_dir = None

    if len(points) > 1:
        first = points[0].value
        last = points[-1].value
        delta = last - first
        if first != 0:
            pct_change = (delta / first) * 100.0
        else:
            pct_change = None

        if delta > 0:
            trend_dir = "increasing"
        elif delta < 0:
            trend_dir = "decreasing"
        else:
            trend_dir = "stable"

    return models.MeasurementTrends(
        metric=metric,
        points=points,
        slope=slope,
        category=category,
        delta=delta,
        pct_change=pct_change,
        trend_dir=trend_dir,
    )


@app.get(
    "/alerts",
    response_model=models.AlertList,
    summary="Get health alerts",
    description="Create simple health alerts based on measurements.",
    tags=["analytics"],
)
def get_alerts(session: Session = Depends(db.get_session)):
    measurements = session.exec(
        select(models.Measurement).order_by(models.Measurement.timestamp)
    ).all()
    alerts = []

    for idx, m in enumerate(measurements):
        if m.body_fat_pct is not None and m.body_fat_pct > 30:
            alerts.append(
                models.AlertItem(
                    measurement_id=m.id,
                    metric="body_fat_pct",
                    value=m.body_fat_pct,
                    message="Body fat > 30%",
                )
            )
        if m.bmi is not None and m.bmi > 30:
            alerts.append(
                models.AlertItem(
                    measurement_id=m.id, metric="bmi", value=m.bmi, message="BMI > 30"
                )
            )
        if idx > 0:
            prev = measurements[idx - 1]
            if m.weight_kg - prev.weight_kg > 2:
                alerts.append(
                    models.AlertItem(
                        measurement_id=m.id,
                        metric="weight_kg",
                        value=m.weight_kg,
                        message="Weight jump > 2kg",
                    )
                )

    return models.AlertList(alerts=alerts)


@app.post(
    "/goals",
    response_model=models.GoalRead,
    status_code=201,
    summary="Create goal",
    description="Create a new target goal.",
    tags=["goals"],
)
def create_goal(payload: models.GoalCreate, session: Session = Depends(db.get_session)):
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
