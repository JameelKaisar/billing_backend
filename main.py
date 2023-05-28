from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_, func
from typing import Dict

from billing import crud, models, schemas
from billing.models import QuarterType, Room, User, Meter, UserToRoom, MeterToRoom, FlatRate, MeterRate, Reading
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

# quarter_type
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

# meter_to_room
@app.post("/meter_to_room/", response_model=schemas.MeterToRoomRead)
def create_meter_to_room(meter_to_room: schemas.MeterToRoomCreate, db: Session = Depends(get_db)):
    meter = db.query(Meter).filter(Meter.meter_id == meter_to_room.meter_id).first()
    if not meter:
        raise HTTPException(status_code=400, detail="Meter does not exist")
    room = db.query(Room).filter(Room.room_id == meter_to_room.room_id).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room does not exist")
    if not room.is_metered:
        raise HTTPException(status_code=400, detail="Room is not metered")
    existing_meter_to_room = db.query(MeterToRoom).filter(MeterToRoom.meter_id == meter_to_room.meter_id,MeterToRoom.room_id == meter_to_room.room_id).first()
    if not existing_meter_to_room:
        try:
            return crud.create_meter_to_room(db=db, meter_to_room=meter_to_room)
        except:
            raise HTTPException(status_code=400, detail="Meter to room already exists")
    else:
        raise HTTPException(status_code=400, detail="Meter to room already exists")
    
@app.get("/meter_to_room/", response_model=schemas.MeterToRoomRead)
def read_meter_to_room(meter_to_room_id: int, db: Session = Depends(get_db)):
    meter_to_room = crud.get_meter_to_room(db, meter_to_room_id)
    if not meter_to_room:
        raise HTTPException(status_code=400, detail="Meter to room not found")
    return meter_to_room

@app.get("/meter_to_rooms/", response_model=list[schemas.MeterToRoomRead])
def get_meter_to_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meter_to_rooms = crud.get_meters_to_rooms(db, skip=skip, limit=limit)
    return meter_to_rooms

@app.put("/meter_to_room/", response_model=schemas.MeterToRoomRead)
def update_meter_to_room(meter_to_room: schemas.MeterToRoomUpdate, db: Session = Depends(get_db)):
    mtr = crud.get_meter_to_room(db, meter_to_room.meter_to_room_id)
    if not mtr:
        raise HTTPException(status_code=400, detail="Meter to room not found")
    meter = db.query(Meter).filter(Meter.meter_id == meter_to_room.meter_id).first()
    if not meter:
        raise HTTPException(status_code=400, detail="Meter does not exist")
    room = db.query(Room).filter(Room.room_id == meter_to_room.room_id).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room does not exist")
    if not room.is_metered:
        raise HTTPException(status_code=400, detail="Room is not metered")
    try:
        return crud.update_meter_to_room(db, meter_to_room)
    except:
        raise HTTPException(status_code=400, detail="Meter to room already exists")
    
@app.delete("/meter_to_room/", response_model=schemas.MeterToRoomRead)
def delete_meter_to_room(meter_to_room: schemas.MeterToRoomDelete, db: Session = Depends(get_db)):
    meter_to_room = crud.get_meter_to_room(db, meter_to_room.meter_to_room_id)
    if not meter_to_room:
        raise HTTPException(status_code=400, detail="Meter to room not found")
    crud.delete_meter_to_room(db, meter_to_room)
    return meter_to_room

# room_creation
@app.post("/room_creation/", response_model=schemas.RoomCreationRead)
def create_room_creation(room_creation: schemas.RoomCreationCreate, db: Session = Depends(get_db)):
    try:
        quarter_type = db.query(QuarterType).filter(QuarterType.quarter_id == room_creation.quarter_type_id).first()
        if not quarter_type:
            raise HTTPException(status_code=400, detail="Quarter type does not exist")
        if room_creation.is_metered:
            mtr_rate = db.query(MeterRate).filter(MeterRate.meter_rate_id == room_creation.meter_rate_id).first()
            if not mtr_rate:
                raise HTTPException(status_code=400, detail="Meter rate does not exist")
        else: 
            flat_rate = db.query(FlatRate).filter(FlatRate.flat_rate_id == room_creation.flat_rate_id).first()
            if not flat_rate:
                raise HTTPException(status_code=400, detail="Flat rate does not exist")
        existing_room = db.query(Room).filter(Room.quarter_type_id == room_creation.quarter_type_id,Room.room_number == room_creation.room_number).first()
        if not existing_room:
            return crud.create_room_creation(db=db, room_creation=room_creation)
        else:
            raise HTTPException(status_code=400, detail="Room already exists")   
    except:
        raise HTTPException(status_code=400, detail="Room creation failed")

# @app.put("/room_creation/", response_model=schemas.RoomCreationRead)
# def update_room_creation(room_creation: schemas.RoomCreationUpdate, db: Session = Depends(get_db)):
#     room_creation = crud.get_room_creation(db, room_creation.room_creation_id)
#     if not room_creation:
#         raise HTTPException(status_code=400, detail="Room not found")
#     try:
#         return crud.update_room_creation(db, room_creation)
#     except:
#         raise HTTPException(status_code=400, detail="Room creation already exists")
    
@app.delete("/room_creation/", response_model=Dict[str, str])
def delete_room_creation(room_creation: schemas.RoomCreationDelete, db: Session = Depends(get_db)):
    room_id = room_creation.room_id
    room_exists = db.query(Room).filter(Room.room_id == room_id).first()
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    crud.delete_room_creation(db, room_creation)
    return room_creation

# flat_rate
@app.post("/flat_rate/", response_model=schemas.FlatRateRead)
def create_flat_rate(flat_rate: schemas.FlatRateCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_flat_rate(db=db, flat_rate=flat_rate)
    except:
        raise HTTPException(status_code=400, detail="Flat Rate Code already exists")


# @app.put("/flat_rate/", response_model=schemas.FlatRateRead)
# def update_flat_rate(flat_rate: schemas.FlatRateUpdate, db: Session = Depends(get_db)):
#     fr = crud.get_flat_rate(db, flat_rate.flat_rate_id)
#     if not fr:
#         raise HTTPException(status_code=400, detail="Flat Rate not found")
#     try:
#         return crud.update_flat_rate(db, flat_rate)
#     except:
#         raise HTTPException(status_code=400, detail="Flat Rate Code already exists")

@app.delete("/flat_rate/", response_model=schemas.FlatRateRead)
def delete_flat_rate(flat_rate: schemas.FlatRateDelete, db: Session = Depends(get_db)):
    flat_rate = crud.get_flat_rate(db, flat_rate.flat_rate_id)
    if not flat_rate:
        raise HTTPException(status_code=400, detail="Flat Rate not found")
    crud.delete_flat_rate(db, flat_rate)
    return flat_rate

# meter_rate
@app.post("/meter_rate/", response_model=schemas.MeterRateRead)
def create_meter_rate(meter_rate: schemas.MeterRateCreate, db: Session = Depends(get_db)):
        mtr_rate = db.query(MeterRate).filter(
                MeterRate.meter_rate_name == meter_rate.meter_rate_name,
                MeterRate.meter_rate_upto == meter_rate.meter_rate_upto
        ).first()
        if not mtr_rate:
            return crud.create_meter_rate(db=db, meter_rate=meter_rate)
        else:
            raise HTTPException(status_code=400, detail="Meter Rate Coding already fed")

@app.get("/meter_rate/", response_model=schemas.MeterRateRead)
def read_meter_rate(meter_rate_id: int, db: Session = Depends(get_db)):
    meter_rate = crud.get_meter_rate(db, meter_rate_id)
    if not meter_rate:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    return meter_rate

@app.get("/meter_rates/", response_model=list[schemas.MeterRateRead])
def get_meter_rates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meter_rates = crud.get_meter_rates(db, skip=skip, limit=limit)
    return meter_rates

@app.put("/meter_rate/", response_model=schemas.MeterRateRead)
def update_meter_rate(meter_rate: schemas.MeterRateUpdate, db: Session = Depends(get_db)):
    mtr_rate = crud.get_meter_rate(db, meter_rate.meter_rate_id)
    if not mtr_rate:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    mtr_rate = db.query(MeterRate).filter(
        MeterRate.meter_rate_name == meter_rate.meter_rate_name,
        MeterRate.meter_rate_upto == meter_rate.meter_rate_upto
    ).first()
    if not mtr_rate:
        return crud.update_meter_rate(db, meter_rate)
    else:
        raise HTTPException(status_code=400, detail="Meter Rate Coding already fed")
    
@app.delete("/meter_rate/", response_model=schemas.MeterRateRead)
def delete_meter_rate(meter_rate: schemas.MeterRateDelete, db: Session = Depends(get_db)):
    meter_rate = crud.get_meter_rate(db, meter_rate.meter_rate_id)
    if not meter_rate:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    crud.delete_meter_rate(db, meter_rate)
    return meter_rate

# flat_rate_to_room
@app.post("/flat_rate_to_room/", response_model=schemas.FlatRateToRoomRead)
def create_flat_rate_to_room(flat_rate_to_room: schemas.FlatRateToRoomCreate, db: Session = Depends(get_db)):
    room_exists = crud.get_room(db, flat_rate_to_room.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    flat_rate_exists = crud.get_flat_rate(db, flat_rate_to_room.flat_rate_id)
    if not flat_rate_exists:
        raise HTTPException(status_code=400, detail="Flat Rate not found")
    room = db.query(Room).filter(Room.room_id == flat_rate_to_room.room_id).first()
    if room.is_metered:
        raise HTTPException(status_code=400, detail="Room is metered")
    try:
        return crud.create_flat_rate_to_room(db=db, flat_rate_to_room=flat_rate_to_room)
    except:
        raise HTTPException(status_code=400, detail="Flat Rate to Room already exists")

@app.get("/flat_rate_to_room/", response_model=schemas.FlatRateToRoomRead)
def read_flat_rate_to_room(flat_rate_to_room_id: int, db: Session = Depends(get_db)):
    flat_rate_to_room = crud.get_flat_rate_to_room(db, flat_rate_to_room_id)
    if not flat_rate_to_room:
        raise HTTPException(status_code=400, detail="Flat Rate to Room not found")
    return flat_rate_to_room

@app.get("/flat_rate_to_rooms/", response_model=list[schemas.FlatRateToRoomRead])
def get_flat_rate_to_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flat_rate_to_rooms = crud.get_flat_rate_to_rooms(db, skip=skip, limit=limit)
    return flat_rate_to_rooms

@app.put("/flat_rate_to_room/", response_model=schemas.FlatRateToRoomRead)
def update_flat_rate_to_room(flat_rate_to_room: schemas.FlatRateToRoomUpdate, db: Session = Depends(get_db)):
    fr_to_room = crud.get_flat_rate_to_room(db, flat_rate_to_room.flat_rate_to_room_id)
    if not fr_to_room:
        raise HTTPException(status_code=400, detail="Flat Rate to Room not found")
    room_exists = crud.get_room(db, flat_rate_to_room.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    flat_rate_exists = crud.get_flat_rate(db, flat_rate_to_room.flat_rate_id)
    if not flat_rate_exists:
        raise HTTPException(status_code=400, detail="Flat Rate not found")
    room = db.query(Room).filter(Room.room_id == flat_rate_to_room.room_id).first()
    if room.is_metered:
        raise HTTPException(status_code=400, detail="Room is metered")
    try:
        return crud.update_flat_rate_to_room(db, flat_rate_to_room)
    except:
        raise HTTPException(status_code=400, detail="Flat Rate to Room already exists")
    
@app.delete("/flat_rate_to_room/", response_model=schemas.FlatRateToRoomRead)
def delete_flat_rate_to_room(flat_rate_to_room: schemas.FlatRateToRoomDelete, db: Session = Depends(get_db)):
    flat_rate_to_room = crud.get_flat_rate_to_room(db, flat_rate_to_room.flat_rate_to_room_id)
    if not flat_rate_to_room:
        raise HTTPException(status_code=400, detail="Flat Rate to Room not found")
    crud.delete_flat_rate_to_room(db, flat_rate_to_room)
    return flat_rate_to_room

# meter rate to room
@app.post("/meter_rate_to_room/", response_model=schemas.MeterRateToRoomRead)
def create_meter_rate_to_room(meter_rate_to_room: schemas.MeterRateToRoomCreate, db: Session = Depends(get_db)):
    room_exists = crud.get_room(db, meter_rate_to_room.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    meter_rate_exists = crud.get_meter_rate(db, meter_rate_to_room.meter_rate_id)
    if not meter_rate_exists:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    room = db.query(Room).filter(Room.room_id == meter_rate_to_room.room_id).first()
    if not room.is_metered:
        raise HTTPException(status_code=400, detail="Room is not metered")
    try:
        return crud.create_meter_rate_to_room(db=db, meter_rate_to_room=meter_rate_to_room)
    except:
        raise HTTPException(status_code=400, detail="Meter Rate to Room already exists")
    
@app.get("/meter_rate_to_room/", response_model=schemas.MeterRateToRoomRead)
def read_meter_rate_to_room(meter_rate_to_room_id: int, db: Session = Depends(get_db)):
    meter_rate_to_room = crud.get_meter_rate_to_room(db, meter_rate_to_room_id)
    if not meter_rate_to_room:
        raise HTTPException(status_code=400, detail="Meter Rate to Room not found")
    return meter_rate_to_room

@app.get("/meter_rate_to_rooms/", response_model=list[schemas.MeterRateToRoomRead])
def get_meter_rate_to_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meter_rate_to_rooms = crud.get_meter_rate_to_rooms(db, skip=skip, limit=limit)
    return meter_rate_to_rooms

@app.put("/meter_rate_to_room/", response_model=schemas.MeterRateToRoomRead)
def update_meter_rate_to_room(meter_rate_to_room: schemas.MeterRateToRoomUpdate, db: Session = Depends(get_db)):
    mr_to_room = crud.get_meter_rate_to_room(db, meter_rate_to_room.meter_rate_to_room_id)
    if not mr_to_room:
        raise HTTPException(status_code=400, detail="Meter Rate to Room not found")
    room_exists = crud.get_room(db, meter_rate_to_room.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    meter_rate_exists = crud.get_meter_rate(db, meter_rate_to_room.meter_rate_id)
    if not meter_rate_exists:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    room = db.query(Room).filter(Room.room_id == meter_rate_to_room.room_id).first()
    if not room.is_metered:
        raise HTTPException(status_code=400, detail="Room is not metered")
    try:
        return crud.update_meter_rate_to_room(db, meter_rate_to_room)
    except:
        raise HTTPException(status_code=400, detail="Meter Rate to Room already exists")
    
@app.delete("/meter_rate_to_room/", response_model=schemas.MeterRateToRoomRead)
def delete_meter_rate_to_room(meter_rate_to_room: schemas.MeterRateToRoomDelete, db: Session = Depends(get_db)):
    meter_rate_to_room = crud.get_meter_rate_to_room(db, meter_rate_to_room.meter_rate_to_room_id)
    if not meter_rate_to_room:
        raise HTTPException(status_code=400, detail="Meter Rate to Room not found")
    crud.delete_meter_rate_to_room(db, meter_rate_to_room)
    return meter_rate_to_room


# reading
# not let user enter reading if it is from previous month -> year <= y & month < m
@app.post("/reading/", response_model=schemas.ReadingRead)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    meter_exists = db.query(Meter).filter(Meter.meter_id == reading.meter_id).first()
    if not meter_exists:
        raise HTTPException(status_code=400, detail="Meter not found")
    reading_exists = db.query(Reading).filter(Reading.meter_id == reading.meter_id, Reading.month == reading.month, Reading.year == reading.year).first()
    if reading_exists:
        raise HTTPException(status_code=400, detail="Reading already exists")
    #check that prev won't get added
    max_year = db.query(func.max(Reading.year)).filter(Reading.meter_id == reading.meter_id).scalar()
    if max_year is not None and reading.year < max_year:
        raise HTTPException(status_code=400, detail="Cannot enter reading for a previous year")
    max_month = db.query(func.max(Reading.month)).filter(Reading.meter_id == reading.meter_id, Reading.year == max_year).scalar()
    if max_month is not None and reading.year == max_year and reading.month < max_month:
        raise HTTPException(status_code=400, detail="Cannot enter reading for a previous month")
    try:
        return crud.create_reading(db=db, reading=reading)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    
@app.get("/reading/", response_model=schemas.ReadingRead)
def read_reading(reading_id: int, db: Session = Depends(get_db)):
    reading = crud.get_reading(db, reading_id)
    if not reading:
        raise HTTPException(status_code=400, detail="Reading not found")
    return reading

@app.get("/readings/", response_model=list[schemas.ReadingRead])
def get_readings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    readings = crud.get_readings(db, skip=skip, limit=limit)
    return readings

@app.put("/reading/", response_model=schemas.ReadingRead)
def update_reading(reading: schemas.ReadingUpdate, db: Session = Depends(get_db)):
    meter_exists = db.query(Meter).filter(Meter.meter_id == reading.meter_id).first()
    if not meter_exists:
        raise HTTPException(status_code=400, detail="Meter not found")
    reading_exists = db.query(Reading).filter(Reading.meter_id == reading.meter_id, Reading.month == reading.month, Reading.year == reading.year).first()
    if not reading_exists:
        return HTTPException(status_code=400, detail="Reading not found")
    if reading_exists.locked:
        return HTTPException(status_code=400, detail="Reading is locked")
    # check if prev reading exists
    max_year = db.query(func.max(Reading.year)).filter(Reading.meter_id == reading.meter_id).scalar()
    if max_year is not None and reading.year < max_year:
        raise HTTPException(status_code=400, detail="Cannot enter reading for a previous year")
    max_month = db.query(func.max(Reading.month)).filter(Reading.meter_id == reading.meter_id, Reading.year == max_year).scalar()
    if max_month is not None and reading.year == max_year and reading.month < max_month:
        raise HTTPException(status_code=400, detail="Cannot enter reading for a previous month")
    try:
        return crud.update_reading(db, reading)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    
@app.delete("/reading/", response_model=schemas.ReadingRead)
def delete_reading(reading: schemas.ReadingDelete, db: Session = Depends(get_db)):
    reading = crud.get_reading(db, reading.reading_id)
    if not reading:
        raise HTTPException(status_code=400, detail="Reading not found")
    crud.delete_reading(db, reading)
    return reading


# bill

# check user_id, meter_id and room_id belong to same user -> not req as we are calculating it ourselves in backend
@app.post("/bill/", response_model=schemas.BillRead)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    room_exists = crud.get_room(db, bill.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    bill_exists = crud.get_bill(db, bill.bill_id)
    if bill_exists:
        raise HTTPException(status_code=400, detail="Bill already exists")
    room_exists = crud.get_room(db, bill.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    meter_exists = crud.get_meter(db, bill.meter_id)
    if not meter_exists:
        raise HTTPException(status_code=400, detail="Meter not found")
    try:
        return crud.create_bill(db=db, bill=bill)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    
@app.get("/bill/", response_model=schemas.BillRead)
def read_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = crud.get_bill(db, bill_id)
    if not bill:
        raise HTTPException(status_code=400, detail="Bill not found")
    return bill

@app.get("/bills/", response_model=list[schemas.BillRead])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bills = crud.get_bills(db, skip=skip, limit=limit)
    return bills
    
@app.delete("/bill/", response_model=schemas.BillRead)
def delete_bill(bill: schemas.BillDelete, db: Session = Depends(get_db)):
    bill = crud.get_bill(db, bill.bill_id)
    if not bill:
        raise HTTPException(status_code=400, detail="Bill not found")
    crud.delete_bill(db, bill)
    return bill