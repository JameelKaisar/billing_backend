from sqlalchemy.orm import Session

from billing import models, schemas


def get_meter(db: Session, meter_id: int):
    return db.query(models.Meter).filter(models.Meter.meter_id == meter_id).first()


def get_meters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meter).offset(skip).limit(limit).all()


def create_meter(db: Session, meter: schemas.MeterCreate):
    initial_reading = meter.initial_reading
    db_meter = models.Meter(initial_reading=initial_reading)
    db.add(db_meter)
    db.commit()
    db.refresh(db_meter)
    return db_meter
