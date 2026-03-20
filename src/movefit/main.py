from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

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

    if not model.bmi and model.weight_kg:
        # height is not provided; BMI cannot be derived safely without height
        pass

    session.add(model)
    session.commit()
    session.refresh(model)
    return model


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
