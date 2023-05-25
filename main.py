from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from billing import crud, models, schemas
from billing.models import QuarterType, Room, User, UserToRoom
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
#user
@app.post("/user/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_users(db=db, user=user)

@app.get("/user/", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@app.get("/users/", response_model=list[schemas.UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/user/", response_model=schemas.UserRead)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    usr = crud.get_user(db, user.user_id)
    if not usr:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.update_user(db, user)

@app.delete("/user/", response_model=schemas.UserRead)
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    usr = crud.get_user(db, user.user_id)
    if not usr:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.delete_user(db, user)

# meter
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

@app.put("/meter/", response_model=schemas.MeterRead)
def update_meter(meter: schemas.MeterUpdate, db: Session = Depends(get_db)):
    mtr = crud.get_meter(db, meter.meter_id)
    if not mtr:
        raise HTTPException(status_code=400, detail="Meter not found")
    return crud.update_meter(db, meter)

@app.delete("/meter/", response_model=schemas.MeterRead)
def delete_meter(meter: schemas.MeterDelete, db: Session = Depends(get_db)):
    meter = crud.get_meter(db, meter.meter_id)
    if not meter:
        raise HTTPException(status_code=400, detail="Meter not found")
    crud.delete_meter(db, meter)
    return meter

# quarter type
@app.post("/quarter_type/", response_model=schemas.QuarterTypeRead)
def create_quarter_type(quarter_type: schemas.QuarterTypeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_quarter_type(db=db, quarter_type=quarter_type)
    except:
        raise HTTPException(status_code=400, detail="Quarter Type already exists")

@app.get("/quarter_type/", response_model=schemas.QuarterTypeRead)
def read_quarter_type(quarter_type_id: int, db: Session = Depends(get_db)):
    quarter_type = crud.get_quarter_type(db, quarter_type_id)
    if not quarter_type:
        raise HTTPException(status_code=400, detail="Quarter Type not found")
    return quarter_type

@app.get("/quarter_types/", response_model=list[schemas.QuarterTypeRead])
def get_quarter_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quarter_types = crud.get_quarter_types(db, skip=skip, limit=limit)
    return quarter_types

@app.put("/quarter_type/", response_model=schemas.QuarterTypeRead)
def update_quarter_type(quarter_type: schemas.QuarterTypeUpdate, db: Session = Depends(get_db)):
    qtr_type = crud.get_quarter_type(db, quarter_type.quarter_id)
    if not qtr_type:
        raise HTTPException(status_code=400, detail="Quarter Type not found")
    return crud.update_quarter_type(db, quarter_type)

@app.delete("/quarter_type/", response_model=schemas.QuarterTypeRead)
def delete_quarter_type(quarter_type: schemas.QuarterTypeDelete, db: Session = Depends(get_db)):
    quarter_type = crud.get_quarter_type(db, quarter_type.quarter_id)
    if not quarter_type:
        raise HTTPException(status_code=400, detail="Quarter Type not found")
    crud.delete_quarter_type(db, quarter_type)
    return quarter_type

# room
@app.post("/room/", response_model=schemas.RoomRead)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    quarter_type = db.query(QuarterType).filter(QuarterType.quarter_id == room.quarter_type_id).first()
    if not quarter_type:
        raise HTTPException(status_code=400, detail="Quarter type does not exist")
    existing_room = db.query(Room).filter(Room.quarter_type_id == room.quarter_type_id,Room.room_number == room.room_number).first()
    if not existing_room:
        return crud.create_room(db=db, room=room)
    else:
        raise HTTPException(status_code=400, detail="Room already exists")

@app.get("/room/", response_model=schemas.RoomRead)
def read_room(room_id: int, db: Session = Depends(get_db)):
    room = crud.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=400, detail="Room not found")
    return room

@app.get("/rooms/", response_model=list[schemas.RoomRead])
def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms

@app.put("/room/", response_model=schemas.RoomRead)
def update_room(room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    rm = crud.get_room(db, room.room_id)
    if not rm:
        raise HTTPException(status_code=400, detail="Room not found")
    return crud.update_room(db, room)

@app.delete("/room/", response_model=schemas.RoomRead)
def delete_room(room: schemas.RoomDelete, db: Session = Depends(get_db)):
    room = crud.get_room(db, room.room_id)
    if not room:
        raise HTTPException(status_code=400, detail="Room not found")
    crud.delete_room(db, room)
    return room

# user_to_room
@app.post("/user_to_room/", response_model=schemas.UserToRoomRead)
def create_user_to_room(user_to_room: schemas.UserToRoomCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_to_room.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    room = db.query(Room).filter(Room.room_id == user_to_room.room_id).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room does not exist")
    existing_user_to_room = db.query(UserToRoom).filter(UserToRoom.user_id == user_to_room.user_id,UserToRoom.room_id == user_to_room.room_id).first()
    if not existing_user_to_room:
        try:
            return crud.create_user_to_room(db=db, user_to_room=user_to_room)
        except:
            raise HTTPException(status_code=400, detail="Room already alloted to someone")
    else:
        raise HTTPException(status_code=400, detail="User to room already exists")

@app.get("/user_to_room/", response_model=schemas.UserToRoomRead)
def read_user_to_room(user_to_room_id: int, db: Session = Depends(get_db)):
    user_to_room = crud.get_user_to_room(db, user_to_room_id)
    if not user_to_room:
        raise HTTPException(status_code=400, detail="User to room not found")
    return user_to_room

@app.get("/user_to_rooms/", response_model=list[schemas.UserToRoomRead])
def get_user_to_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_to_rooms = crud.get_users_to_rooms(db, skip=skip, limit=limit)
    return user_to_rooms

@app.put("/user_to_room/", response_model=schemas.UserToRoomRead)
def update_user_to_room(user_to_room: schemas.UserToRoomUpdate, db: Session = Depends(get_db)):
    utr = crud.get_user_to_room(db, user_to_room.user_to_room_id)
    if not utr:
        raise HTTPException(status_code=400, detail="User to room not found")
    user = db.query(User).filter(User.user_id == user_to_room.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    room = db.query(Room).filter(Room.room_id == user_to_room.room_id).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room does not exist")
    try:
        return crud.update_user_to_room(db, user_to_room)
    except:
        raise HTTPException(status_code=400, detail="User to room already exists")
@app.delete("/user_to_room/", response_model=schemas.UserToRoomRead)
def delete_user_to_room(user_to_room: schemas.UserToRoomDelete, db: Session = Depends(get_db)):
    user_to_room = crud.get_user_to_room(db, user_to_room.user_to_room_id)
    if not user_to_room:
        raise HTTPException(status_code=400, detail="User to room not found")
    crud.delete_user_to_room(db, user_to_room)
    return user_to_room