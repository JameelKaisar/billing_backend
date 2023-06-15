from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, not_
from datetime import timedelta
from typing import Dict, List

from billing import crud, schemas
from billing.common import get_db
from billing.database import engine
from billing.const import ACCESS_TOKEN_EXPIRE_MINUTES
from billing.auth import get_current_active_user, authenticate_user, create_access_token
from billing.models import Base, User, QuarterType, Room, Meter, UserToRoom, MeterToRoom, FlatRate, MeterRate, Reading, Department, UserToDepartment, UnmeteredBill, MeteredBill



Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



# test
@app.get("/")
def read_root():
    return {"Hello": "World"}


# auth
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# user
@app.get("/users/me/", response_model=schemas.UserBase)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: schemas.UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


# user
@app.post("/user/", response_model=schemas.UserBase)
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

# @app.put("/user/", response_model=schemas.UserRead)
# def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     usr = crud.get_user(db, user.user_id)
#     if not usr:
#         raise HTTPException(status_code=400, detail="User not found")
#     return crud.update_user(db, user)

@app.delete("/user/", response_model=schemas.UserRead)
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    usr = crud.get_user(db, user.user_id)
    if not usr:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.delete_user(db, user)

# department

@app.post("/department/", response_model=schemas.DepartmentRead)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    dept = db.query(Department).filter(Department.department_name == department.department_name).first()
    if not dept:
    # try:
        return crud.create_department(db=db, department=department)
    # except:
    raise HTTPException(status_code=400, detail="Department already exists")

@app.get("/department/", response_model=schemas.DepartmentRead)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = crud.get_department(db, department_id)
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")
    return department

@app.get("/departments/", response_model=list[schemas.DepartmentRead])
def get_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments

@app.put("/department/", response_model=schemas.DepartmentRead)
def update_department(department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    dept = crud.get_department(db, department.department_id)
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found")
    dept = db.query(Department).filter(Department.department_name == department.department_name).first()
    if not dept:
        return crud.update_department(db, department)
    raise HTTPException(status_code=400, detail="Department already exists")

@app.delete("/department/", response_model=schemas.DepartmentRead)
def delete_department(department: schemas.DepartmentDelete, db: Session = Depends(get_db)):
    try:
        return crud.delete_department(db, department)
    except:
        raise HTTPException(status_code=400, detail="Department not found")
    
# user to department
# check if user exists and dept exists
@app.post("/user_to_department/", response_model=schemas.UserToDepartmentRead)
def create_user_to_department(user_department: schemas.UserToDepartmentCreate, db: Session = Depends(get_db)):
    exists = db.query(UserToDepartment).filter(UserToDepartment.user_id == user_department.user_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="UserToDepartment already exists")
    user_exists = db.query(User).filter(User.user_id == user_department.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found")
    dept_exists = db.query(Department).filter(Department.department_id == user_department.department_id).first()
    if not dept_exists:
        raise HTTPException(status_code=400, detail="Department not found")
    return crud.create_user_to_department(db=db, user_to_department=user_department)
    

@app.get("/user_to_department/", response_model=schemas.UserToDepartmentRead)
def read_user_to_department(user_to_department_id: int, db: Session = Depends(get_db)):
    user_to_department = crud.get_user_to_department(db, user_to_department_id)
    if not user_to_department:
        raise HTTPException(status_code=400, detail="UserToDepartment not found")
    return user_to_department

@app.get("/user_to_departments/", response_model=list[schemas.UserToDepartmentRead])
def get_user_to_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_to_departments = crud.get_user_to_departments(db, skip=skip, limit=limit)
    return user_to_departments

@app.put("/user_to_department/", response_model=schemas.UserToDepartmentRead)
def update_user_to_department(user_to_department: schemas.UserToDepartmentUpdate, db: Session = Depends(get_db)):
    usr_dept = crud.get_user_to_department(db, user_to_department.user_to_department_id)
    if not usr_dept:
        raise HTTPException(status_code=400, detail="UserToDepartment not found")
    user_exists = db.query(User).filter(User.user_id == user_to_department.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=400, detail="User not found")
    dept_exists = db.query(Department).filter(Department.department_id == user_to_department.department_id).first()
    if not dept_exists:
        raise HTTPException(status_code=400, detail="Department not found")
    user_dept = db.query(UserToDepartment).filter(UserToDepartment.user_id == user_to_department.user_id, UserToDepartment.department_id == user_to_department.department_id).first()
    if user_dept:
        raise HTTPException(status_code=400, detail="User already has same Department")
    return crud.update_user_to_department(db, user_to_department)

@app.delete("/user_to_department/", response_model=schemas.UserToDepartmentRead)
def delete_user_to_department(user_to_department: schemas.UserToDepartmentDelete, db: Session = Depends(get_db)):
    usr_dept = crud.get_user_to_department(db, user_to_department.user_to_department_id)
    if not usr_dept:
        raise HTTPException(status_code=400, detail="UserToDepartment not found")
    return crud.delete_user_to_department(db, user_to_department)

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
@app.get("/room_creation_metered/", response_model=schemas.RoomCreationReadMetered)
def read_room_creation_metered(room_creation_id: int, db: Session = Depends(get_db)):
    room_creation = crud.get_room_creation_metered(db, room_creation_id)
    if not room_creation:
        raise HTTPException(status_code=400, detail="Metered Room not found")
    return room_creation

@app.get("/room_creations_metered/", response_model=list[schemas.RoomCreationReadMetered])
def read_room_creations_metered(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    room_creations = crud.get_room_creations_metered(db, skip=skip, limit=limit)
    return room_creations

@app.get("/room_creation_unmetered/", response_model=schemas.RoomCreationReadUnmetered)
def read_room_creation_unmetered(room_creation_id: int, db: Session = Depends(get_db)):
    room_creation = crud.get_room_creation_unmetered(db, room_creation_id)
    if not room_creation:
        raise HTTPException(status_code=400, detail="Unmetered Room not found")
    return room_creation

@app.get("/room_creations_unmetered/", response_model=list[schemas.RoomCreationReadUnmetered])
def read_room_creations_unmetered(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    room_creations = crud.get_room_creations_unmetered(db, skip=skip, limit=limit)
    return room_creations

@app.delete("/room_creation/", response_model=Dict[str, str])
def delete_room_creation(room_creation: schemas.RoomCreationDelete, db: Session = Depends(get_db)):
    room_id = room_creation.room_id
    room_exists = db.query(Room).filter(Room.room_id == room_id).first()
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    crud.delete_room_creation(db, room_creation)
    return room_creation

# user creation
@app.post("/user_creation/", response_model=schemas.UserCreationRead)
def create_user_creation(user_creation: schemas.UserCreationCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_creation.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_room = db.query(Room).filter(Room.room_id == user_creation.room_id).first()
    if not db_room:
        raise HTTPException(status_code=400, detail="Room does not exist")
    db_department = db.query(Department).filter(Department.department_id == user_creation.department_id).first()
    if not db_department:
        raise HTTPException(status_code=400, detail="Department does not exist")
    try:
        return crud.create_user_creation(db=db, user_creation=user_creation)
    except:
        raise HTTPException(status_code=400, detail="User creation failed")

@app.delete("/user_creation/", response_model=Dict[str, str])
def delete_user_creation(user_creation: schemas.UserCreationDelete, db: Session = Depends(get_db)):
    db_user_creation = crud.get_user_creation(db, user_creation.user_creation_id)
    if db_user_creation is None:
        raise HTTPException(status_code=404, detail="User creation not found")
    crud.delete_user_creation(db, user_creation)
    return user_creation

# flat_rate
@app.post("/flat_rate/")
def create_flat_rate(flat_rate: schemas.FlatRateCreate, db: Session = Depends(get_db)):
    # try:
    return crud.create_flat_rate(db=db, flat_rate=flat_rate)
    # except:
    #     raise HTTPException(status_code=400, detail="Flat Rate Code already exists")

@app.get("/flat_rate/", response_model=schemas.FlatRateRead)
def read_flat_rate(flat_rate_name: str, db: Session = Depends(get_db)):
    flat_rate = crud.get_flat_rate(db, flat_rate_name)
    if not flat_rate:
        raise HTTPException(status_code=400, detail="Flat Rate not found")
    return flat_rate

@app.get("/flat_rates/", response_model=list[schemas.FlatRateRead])
def get_flat_rates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flat_rates = crud.get_flat_rates(db, skip=skip, limit=limit)
    return flat_rates

@app.put("/flat_rate/")
def update_flat_rate(flat_rate: schemas.FlatRateUpdate, db: Session = Depends(get_db)):
    fr = crud.get_flat_rate(db, flat_rate.flat_rate_name)
    if not fr:
        raise HTTPException(status_code=400, detail="Flat Rate not found")
    try:
        return crud.update_flat_rate(db, flat_rate)
    except:
        raise HTTPException(status_code=400, detail="Flat Rate Code already exists")

@app.delete("/flat_rate/")
def delete_flat_rate(flat_rate: schemas.FlatRateDelete, db: Session = Depends(get_db)):
    try:
        flat_rte = crud.get_flat_rate(db, flat_rate.flat_rate_name)
        if not flat_rte:
            raise HTTPException(status_code=400, detail="Flat Rate not found")
        crud.delete_flat_rate(db, flat_rate)
        return flat_rate
    except:
        raise HTTPException(status_code=400, detail="Flat Rate Code doesn't exist")

# meter_rate
@app.post("/meter_rate/")
def create_meter_rate(meter_rate: schemas.MeterRateCreate, db: Session = Depends(get_db)):
        mtr_rate = db.query(MeterRate).filter(
                MeterRate.meter_rate_name == meter_rate.meter_rate_name,
        ).first()
        if not mtr_rate:
            return crud.create_meter_rate(db=db, meter_rate=meter_rate)
        else:
            raise HTTPException(status_code=400, detail="Meter Rate Coding already fed")

@app.get("/meter_rate/", response_model=schemas.MeterRateRead)
def read_meter_rate(meter_rate_name: str, db: Session = Depends(get_db)):
    meter_rate = crud.get_meter_rate(db, meter_rate_name)
    if not meter_rate:
        raise HTTPException(status_code=400, detail="Meter Rate not found")
    return meter_rate

@app.get("/meter_rates/", response_model=list[schemas.MeterRateRead])
def get_meter_rates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meter_rates = crud.get_meter_rates(db, skip=skip, limit=limit)
    return meter_rates

@app.put("/meter_rate/")
def update_meter_rate(meter_rate: schemas.MeterRateUpdate, db: Session = Depends(get_db)):
    return crud.update_meter_rate(db, meter_rate)
    # mtr_rate = crud.get_meter_rate(db, meter_rate.meter_rate_name)
    # if not mtr_rate:
    #     raise HTTPException(status_code=400, detail="Meter Rate not found")
    # mtr_rate = db.query(MeterRate).filter(
    #     MeterRate.meter_rate_name == meter_rate.meter_rate_name,
    #     MeterRate.meter_rate_upto == meter_rate.meter_rate_upto
    # ).first()
    # if not mtr_rate:
    # else:
    #     raise HTTPException(status_code=400, detail="Meter Rate Coding already fed")
    
@app.delete("/meter_rate/")
def delete_meter_rate(meter_rate: schemas.MeterRateDelete, db: Session = Depends(get_db)):
    try:
        mtr_rate = crud.get_meter_rate(db, meter_rate.meter_rate_name)
        if not mtr_rate:
            raise HTTPException(status_code=400, detail="Meter Rate not found")
        crud.delete_meter_rate(db, meter_rate)
        return meter_rate
    except:
        raise HTTPException(status_code=400, detail="Meter Rate not found")

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

@app.post("/unmetered_bill/", response_model=schemas.UnmeteredBillRead)
def create_unmetered_bill(unmetered_bills: schemas.UnmeteredBillCreate, db: Session = Depends(get_db)):
    room_exists = crud.get_room(db, unmetered_bills.room_id)
    if not room_exists:
        raise HTTPException(status_code=400, detail="Room not found")
    unmetered_bill_exists = db.query(UnmeteredBill).filter(UnmeteredBill.room_id == unmetered_bills.room_id, UnmeteredBill.month == unmetered_bills.month, UnmeteredBill.year == unmetered_bills.year).first()
    if unmetered_bill_exists:
        raise HTTPException(status_code=400, detail="Unmetered bill already exists")
    try:
        return crud.create_unmetered_bill(db=db, unmetered_bill=unmetered_bills)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    
@app.get("/unmetered_bill/", response_model=schemas.UnmeteredBillRead)
def read_unmetered_bill(unmetered_bill_id: int, db: Session = Depends(get_db)):
    unmetered_bill = crud.get_unmetered_bill(db, unmetered_bill_id)
    if not unmetered_bill:
        raise HTTPException(status_code=400, detail="Unmetered bill not found")
    return unmetered_bill

@app.get("/unmetered_bills/", response_model=list[schemas.UnmeteredBillRead])
def get_unmetered_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    unmetered_bills = crud.get_unmetered_bills(db, skip=skip, limit=limit)
    return unmetered_bills

@app.delete("/unmetered_bill/", response_model=schemas.UnmeteredBillRead)
def delete_unmetered_bill(unmetered_bill: schemas.UnmeteredBillDelete, db: Session = Depends(get_db)):
    unmetered_bill = crud.get_unmetered_bill(db, unmetered_bill.unmetered_bill_id)
    if not unmetered_bill:
        raise HTTPException(status_code=400, detail="Unmetered bill not found")
    crud.delete_unmetered_bill(db, unmetered_bill)
    return unmetered_bill


# metered_bill

@app.post("/metered_bill/", response_model=schemas.MeteredBillRead)
def create_metered_bill(metered_bill: schemas.MeteredBillCreate, db: Session = Depends(get_db)):
    meter_exists = crud.get_meter(db, metered_bill.meter_id)
    if not meter_exists:
        raise HTTPException(status_code=400, detail="Meter not found")
    metered_bill_exists = db.query(MeteredBill).filter(MeteredBill.meter_id == metered_bill.meter_id, MeteredBill.month == metered_bill.month, MeteredBill.year == metered_bill.year).first()
    if metered_bill_exists:
        raise HTTPException(status_code=400, detail="Metered bill already exists")
    try:
        return crud.create_metered_bill(db=db, metered_bill=metered_bill)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    
    
@app.get("/metered_bill/", response_model=schemas.MeteredBillRead)
def read_metered_bill(metered_bill_id: int, db: Session = Depends(get_db)):
    metered_bill = crud.get_metered_bill(db, metered_bill_id)
    if not metered_bill:
        raise HTTPException(status_code=400, detail="Metered bill not found")
    return metered_bill

@app.get("/metered_bills/", response_model=list[schemas.MeteredBillRead])
def get_metered_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metered_bills = crud.get_metered_bills(db, skip=skip, limit=limit)
    return metered_bills

@app.delete("/metered_bill/", response_model=schemas.MeteredBillRead)
def delete_metered_bill(metered_bill: schemas.MeteredBillDelete, db: Session = Depends(get_db)):
    metered_bill = crud.get_metered_bill(db, metered_bill.metered_bill_id)
    if not metered_bill:
        raise HTTPException(status_code=400, detail="Metered bill not found")
    crud.delete_metered_bill(db, metered_bill)
    return metered_bill

# bulk generate bills

@app.post("/generate_bulk_metered_bills/")
def generate_bulk_metered_bills(bulk_generate_bills: schemas.BulkMeteredBillCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_bulk_metered_bill(db=db, metered_bill=bulk_generate_bills)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    

@app.post("/generate_bulk_unmetered_bills/")
def generate_bulk_unmetered_bills(bulk_generate_bills: schemas.BulkUnmeteredBillCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_bulk_unmetered_bill(db=db, unmetered_bill=bulk_generate_bills)
    except:
        raise HTTPException(status_code=400, detail="Something went wrong :(")
    

# FETCH REQUEST : QuarterID , RoomNO ==> RoomID
@app.get("/get_room_id_from_room_no/", response_model=List[schemas.QuarterToRoomRead])
def get_room_id_from_room_no(room_number: int, quarter_id: int, db: Session = Depends(get_db)):
    room = crud.get_room_id_from_room_no(db, room_number, quarter_id)
    if not room:
        raise HTTPException(status_code=400, detail="Room not found")
    return [
        schemas.QuarterToRoomRead(
            room_number=room_number,
            quarter_id=quarter_id,
            room_id=room_id,
            is_metered=is_metered
        )
        for room_id, is_metered in room
    ]
    
# FETCH REQUEST : RoomID ==> MeterID
@app.get("/get_meter_id_from_room_id/", response_model=schemas.RoomToMeterRead)
def get_meter_id_from_room_id(room_id: int, db: Session = Depends(get_db)):
    meter_id = crud.get_meter_id_from_room_id(db, room_id)
    if meter_id is None:
        raise HTTPException(status_code=400, detail="Meter not found")
    
    return schemas.RoomToMeterRead(
        room_id=room_id,
        meter_id=meter_id
    )
