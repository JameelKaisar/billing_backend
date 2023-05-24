from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from billing import crud, models, schemas
from billing.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/meter/", response_model=schemas.MeterRead)
def create_meter(meter: schemas.MeterCreate, db: Session = Depends(get_db)):
    return crud.create_meter(db=db, meter=meter)


@app.get("/meter/", response_model=schemas.MeterRead)
def read_meter(meter_id: int, db: Session = Depends(get_db)):
    meter = crud.get_meter(db, meter_id)
    if not meter:
        raise HTTPException(status_code=400, detail="Meter not found")
    return meter


@app.get("/meters/", response_model=list[schemas.MeterRead])
def get_meters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meters = crud.get_meters(db, skip=skip, limit=limit)
    return meters
