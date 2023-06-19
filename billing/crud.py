from sqlalchemy.orm import Session
from sqlalchemy import func, delete, select
from billing import models, schemas
from billing.auth import get_password_hash



# user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# handle existing username (like init.py)
def create_users(db: Session, user: schemas.UserCreate):
    username = user.username
    password = user.password
    hashed_password = get_password_hash(password)
    full_name = user.full_name
    disabled = user.disabled
    access = user.access
    db_user = models.User(username=username, hashed_password=hashed_password, full_name=full_name, disabled=disabled, access=access)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def update_user(db: Session, user: schemas.UserUpdate):
#     user_id = user.user_id
#     user_name = user.user_name
#     db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
#     db_user.user_name = user_name
#     db.commit()
#     db.refresh(db_user)
#     return db_user

def delete_user(db: Session, user: schemas.UserDelete):
    user_id = user.user_id
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
# department
def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.department_id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: schemas.DepartmentCreate):
    department_name = department.department_name
    db_department = models.Department(department_name=department_name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department: schemas.DepartmentUpdate):
    department_id = department.department_id
    department_name = department.department_name
    db_department = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    db_department.department_name = department_name
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department: schemas.DepartmentDelete):
    department_id = department.department_id
    db_department = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    db.delete(db_department)
    db.commit()
    return db_department

# user to department
def get_user_to_department(db: Session, user_to_department_id: int):
    return db.query(models.UserToDepartment).filter(models.UserToDepartment.user_to_department_id == user_to_department_id).first()

def get_user_to_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserToDepartment).offset(skip).limit(limit).all()

def create_user_to_department(db: Session, user_to_department: schemas.UserToDepartmentCreate):
    user_id = user_to_department.user_id
    department_id = user_to_department.department_id
    db_user_to_department = models.UserToDepartment(user_id=user_id, department_id=department_id)
    db.add(db_user_to_department)
    db.commit()
    db.refresh(db_user_to_department)
    return db_user_to_department

def update_user_to_department(db: Session, user_to_department: schemas.UserToDepartmentUpdate):
    user_to_department_id = user_to_department.user_to_department_id
    user_id = user_to_department.user_id
    department_id = user_to_department.department_id
    db_user_to_department = db.query(models.UserToDepartment).filter(models.UserToDepartment.user_to_department_id == user_to_department_id).first()
    db_user_to_department.user_id = user_id
    db_user_to_department.department_id = department_id
    db.commit()
    db.refresh(db_user_to_department)
    return db_user_to_department

def delete_user_to_department(db: Session, user_to_department: schemas.UserToDepartmentDelete):
    user_to_department_id = user_to_department.user_to_department_id
    db_user_to_department = db.query(models.UserToDepartment).filter(models.UserToDepartment.user_to_department_id == user_to_department_id).first()
    db.delete(db_user_to_department)
    db.commit()
    return db_user_to_department

# meter
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

def update_meter(db: Session, meter: schemas.MeterUpdate):
    meter_id = meter.meter_id
    initial_reading = meter.initial_reading
    db_meter = db.query(models.Meter).filter(models.Meter.meter_id == meter_id).first()
    db_meter.initial_reading = initial_reading
    db.commit()
    db.refresh(db_meter)
    return db_meter

def delete_meter(db: Session, meter: schemas.MeterDelete):
    meter_id = meter.meter_id
    db_meter = db.query(models.Meter).filter(models.Meter.meter_id == meter_id).first()
    db.delete(db_meter)
    db.commit()
    return db_meter

# quarter type
def get_quarter_type(db: Session, quarter_id: int):
    return db.query(models.QuarterType).filter(models.QuarterType.quarter_id == quarter_id).first()

def get_quarter_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.QuarterType).offset(skip).limit(limit).all()

def create_quarter_type(db: Session, quarter_type: schemas.QuarterTypeCreate):
    quarter_name = quarter_type.quarter_name
    db_quarter_type = models.QuarterType(quarter_name=quarter_name)
    db.add(db_quarter_type)
    db.commit()
    db.refresh(db_quarter_type)
    return db_quarter_type

def update_quarter_type(db: Session, quarter_type: schemas.QuarterTypeUpdate):
    quarter_id = quarter_type.quarter_id
    quarter_name = quarter_type.quarter_name
    db_quarter_type = db.query(models.QuarterType).filter(models.QuarterType.quarter_id == quarter_id).first()
    db_quarter_type.quarter_name = quarter_name
    db.commit()
    db.refresh(db_quarter_type)
    return db_quarter_type

def delete_quarter_type(db: Session, quarter_type: schemas.QuarterTypeDelete):
    quarter_id = quarter_type.quarter_id
    db_quarter_type = db.query(models.QuarterType).filter(models.QuarterType.quarter_id == quarter_id).first()
    db.delete(db_quarter_type)
    db.commit()
    return db_quarter_type

# room
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.room_id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    quarter_type_id = room.quarter_type_id
    room_number = room.room_number
    is_metered = room.is_metered
    db_rooms = models.Room(quarter_type_id=quarter_type_id, room_number=room_number, is_metered=is_metered)
    db.add(db_rooms)
    db.commit()
    db.refresh(db_rooms)
    return db_rooms
    
def update_room(db: Session, room: schemas.RoomUpdate):
    room_id = room.room_id
    quarter_type_id = room.quarter_type_id
    room_number = room.room_number
    is_metered = room.is_metered
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    db_room.quarter_type_id = quarter_type_id
    db_room.room_number = room_number
    db_room.is_metered = is_metered
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, room: schemas.RoomDelete):
    room_id = room.room_id
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    db.delete(db_room)
    db.commit()
    return db_room

#user to room
def get_user_to_room(db: Session, user_to_room_id: int):
    return db.query(models.UserToRoom).filter(models.UserToRoom.user_to_room_id == user_to_room_id).first()

def get_users_to_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserToRoom).offset(skip).limit(limit).all()

def create_user_to_room(db: Session, user_to_room: schemas.UserToRoomCreate):
    user_id = user_to_room.user_id
    room_id = user_to_room.room_id
    #chck if user is already in room
    db_user_to_room = models.UserToRoom(user_id=user_id, room_id=room_id)
    db.add(db_user_to_room)
    db.commit()
    db.refresh(db_user_to_room)
    return db_user_to_room
        
def update_user_to_room(db: Session, user_to_room: schemas.UserToRoomUpdate):
    user_id = user_to_room.user_id
    room_id = user_to_room.room_id
    #if exists and try except in user to room
    db_user_to_room = db.query(models.UserToRoom).filter(models.UserToRoom.user_id == user_id).first()
    db_user_to_room.room_id = room_id
    db.commit()
    db.refresh(db_user_to_room)
    return db_user_to_room

def delete_user_to_room(db: Session, user_to_room: schemas.UserToRoomDelete):
    user_id = user_to_room.user_id
    db_user_to_room = db.query(models.UserToRoom).filter(models.UserToRoom.user_id == user_id).first()
    db.delete(db_user_to_room)
    db.commit()
    return db_user_to_room

#meter to room
def get_meter_to_room(db: Session, meter_to_room_id: int):
    return db.query(models.MeterToRoom).filter(models.MeterToRoom.meter_to_room_id == meter_to_room_id).first()

def get_meters_to_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MeterToRoom).offset(skip).limit(limit).all()

def create_meter_to_room(db: Session, meter_to_room: schemas.MeterToRoomCreate):
    meter_id = meter_to_room.meter_id
    room_id = meter_to_room.room_id
    db_meter_to_room = models.MeterToRoom(meter_id=meter_id, room_id=room_id)
    db.add(db_meter_to_room)
    db.commit()
    db.refresh(db_meter_to_room)
    return db_meter_to_room

def update_meter_to_room(db: Session, meter_to_room: schemas.MeterToRoomUpdate):
    meter_id = meter_to_room.meter_id
    room_id = meter_to_room.room_id
    db_meter_to_room = db.query(models.MeterToRoom).filter(models.MeterToRoom.meter_id == meter_id).first()
    db_meter_to_room.room_id = room_id
    db.commit()
    db.refresh(db_meter_to_room)
    return db_meter_to_room

def delete_meter_to_room(db: Session, meter_to_room: schemas.MeterToRoomDelete):
    meter_id = meter_to_room.meter_id
    db_meter_to_room = db.query(models.MeterToRoom).filter(models.MeterToRoom.meter_id == meter_id).first()
    db.delete(db_meter_to_room)
    db.commit()
    return db_meter_to_room

# Room Creation
def create_room_creation(db: Session, room_creation: schemas.RoomCreationCreate):
    quarter_type_id = room_creation.quarter_type_id
    room_number = room_creation.room_number
    is_metered = room_creation.is_metered
    db_rooms = models.Room(quarter_type_id=quarter_type_id, room_number=room_number, is_metered=is_metered)
    db.add(db_rooms)
    db.flush()
    room_id = db_rooms.room_id
    if is_metered:
        initial_reading = room_creation.initial_reading
        meter_rate_id = room_creation.meter_rate_id
        db_meter = models.Meter(initial_reading=initial_reading)
        db.add(db_meter)
        db.flush()
        meter_id=db_meter.meter_id
        db_meter_to_room = models.MeterToRoom(meter_id=meter_id, room_id=db_rooms.room_id)
        db.add(db_meter_to_room)
        db_meter_rate_to_room = models.MeterRateToRoom(meter_rate_id=meter_rate_id, room_id=room_id)
        db.add(db_meter_rate_to_room)
    elif not is_metered:
        flat_rate_id = room_creation.flat_rate_id
        db_flat_rate_to_room = models.FlatRateToRoom(flat_rate_id=flat_rate_id, room_id=room_id)
        db.add(db_flat_rate_to_room)    
    db.commit() 
    db.refresh(db_rooms)
    if is_metered:
        db.refresh(db_meter)
        db.refresh(db_meter_to_room)
        db.refresh(db_meter_rate_to_room)
    else:
        db.refresh(db_flat_rate_to_room)
    return db_rooms

def get_room_creation_metered(db: Session, room_id: int):
    try:
        db_rooms = db.query(models.Room).filter(models.Room.room_id == room_id).first()
        db_meter_to_room = db.query(models.MeterToRoom).filter(models.MeterToRoom.room_id == room_id).first()
        db_meter = db.query(models.Meter).filter(models.Meter.meter_id == db_meter_to_room.meter_id).first()
        db_meter_rate_to_room = db.query(models.MeterRateToRoom).filter(models.MeterRateToRoom.room_id == room_id).first()
        db_meter_rate = db.query(models.MeterRate).filter(models.MeterRate.meter_rate_id == db_meter_rate_to_room.meter_rate_id).first()
        # db_meter_rate_type = db.query(models.MeterRateType).filter(models.MeterRateType.meter_rate_type_id == db_meter_rate.meter_rate_type_id).first()
        return {
            "room_id": db_rooms.room_id,
            "quarter_type_id": db_rooms.quarter_type_id,
            "quarter_type_name": db_rooms.quarter_type.quarter_name,
            "room_number": db_rooms.room_number,
            "is_metered": db_rooms.is_metered,
            "initial_reading": db_meter.initial_reading,
            # "meter_rate_id": db_meter_rate_to_room.meter_rate_id,
            "meter_rate_name": db_meter_rate.meter_rate_name,
        }
    except Exception as e:
        return None

def get_room_creations_metered(db: Session, skip: int = 0, limit: int = 100):
    try:
        db_rooms = db.query(models.Room).filter(models.Room.is_metered == True).offset(skip).limit(limit).all()

        room_details = []
        for room in db_rooms:
            db_meter_to_room = db.query(models.MeterToRoom).filter(models.MeterToRoom.room_id == room.room_id).first()
            db_meter = db.query(models.Meter).filter(models.Meter.meter_id == db_meter_to_room.meter_id).first()
            db_meter_rate_to_room = db.query(models.MeterRateToRoom).filter(models.MeterRateToRoom.room_id == room.room_id).first()
            db_meter_rate = db.query(models.MeterRate).filter(models.MeterRate.meter_rate_id == db_meter_rate_to_room.meter_rate_id).first()

            room_details.append({
                "room_id": room.room_id,
                "quarter_type_id": room.quarter_type_id,
                "quarter_type_name": room.quarter_type.quarter_name,
                "room_number": room.room_number,
                "is_metered": room.is_metered,
                "initial_reading": db_meter.initial_reading,
                "meter_rate_name": db_meter_rate.meter_rate_name,
            })

        return room_details
    except Exception as e:
        return None


def get_room_creation_unmetered(db: Session, room_id: int):
    try:
        db_rooms = db.query(models.Room).filter(models.Room.room_id == room_id).first()
        db_flat_rate_to_room = db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.room_id == room_id).first()
        db_flat_rate = db.query(models.FlatRate).filter(models.FlatRate.flat_rate_id == db_flat_rate_to_room.flat_rate_id).first()
        return {
            "room_id": db_rooms.room_id,
            "quarter_type_id": db_rooms.quarter_type_id,
            "quarter_type_name": db_rooms.quarter_type.quarter_name,
            "room_number": db_rooms.room_number,
            "is_metered": db_rooms.is_metered,
            "flat_rate_name": db_flat_rate.flat_rate_name,
        }
    except Exception as e:
        return None

def get_room_creations_unmetered(db: Session, skip: int = 0, limit: int = 100):
    try:
        db_rooms = db.query(models.Room).filter(models.Room.is_metered == False).offset(skip).limit(limit).all()

        room_details = []
        for room in db_rooms:
            db_flat_rate_to_room = db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.room_id == room.room_id).first()
            db_flat_rate = db.query(models.FlatRate).filter(models.FlatRate.flat_rate_id == db_flat_rate_to_room.flat_rate_id).first()

            room_details.append({
                "room_id": room.room_id,
                "quarter_type_id": room.quarter_type_id,
                "quarter_type_name": room.quarter_type.quarter_name,
                "room_number": room.room_number,
                "is_metered": room.is_metered,
                "flat_rate_name": db_flat_rate.flat_rate_name,
            })

        return room_details
    except Exception as e:
        return None

def delete_room_creation(db: Session, room_creation: schemas.RoomCreationDelete):
    room_id = room_creation.room_id
    db_rooms = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    is_metered = db_rooms.is_metered
    if is_metered:
        db_meter_to_room = db.query(models.MeterToRoom).filter(models.MeterToRoom.room_id == room_id).first()
        if db_meter_to_room:
            meter_id = db_meter_to_room.meter_id
            db_meter_rate_to_room = (
                db.query(models.MeterRateToRoom)
                .filter(models.MeterRateToRoom.room_id == room_id)
                .first()
            )
            db_meter = db.query(models.Meter).filter(models.Meter.meter_id == meter_id).first()
            if db_meter_rate_to_room and db_meter:
                db.delete(db_meter_rate_to_room)
                db.delete(db_meter_to_room)
                db.delete(db_meter)
    else:
        db_flat_rate_to_room = db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.room_id == room_id).first()
        if db_flat_rate_to_room:
            db.delete(db_flat_rate_to_room)
    db.delete(db_rooms)
    db.commit()
    return {"message": "Room deletion successful"}

# user creation
def create_user_creation(db: Session, user_creation: schemas.UserCreationCreate):
    username = user_creation.username
    password = user_creation.password
    full_name = user_creation.full_name
    disabled = user_creation.disabled
    hashed_password = get_password_hash(password)
    db_user = models.User(username=username, hashed_password=hashed_password, full_name=full_name, disabled=disabled)
    db.add(db_user)
    db.flush()
    dpt_id = user_creation.department_id
    db_user_to_department = models.UserToDepartment(user_id=db_user.user_id, department_id=dpt_id)
    db.add(db_user_to_department)
    db.flush()
    rm_id = user_creation.room_id
    db_user_to_room = models.UserToRoom(user_id=db_user.user_id, room_id=rm_id)
    db.add(db_user_to_room)
    db.flush()
    db.commit()
    db.refresh(db_user)
    db.refresh(db_user_to_department)
    db.refresh(db_user_to_room)
    return db_user

def delete_user_creation(db: Session, user_creation: schemas.UserCreationDelete):
    user_id = user_creation.user_id
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user_to_department = db.query(models.UserToDepartment).filter(models.UserToDepartment.user_id == user_id).first()
    db_user_to_room = db.query(models.UserToRoom).filter(models.UserToRoom.user_id == user_id).first()
    db.delete(db_user_to_department)
    db.delete(db_user_to_room)
    db.delete(db_user)
    db.commit()
    return {"message": "User deletion successful"}


# flat_rate
def get_flat_rate(db: Session, flat_rate_name: str):
    
    flat_rates = db.query(models.FlatRate).filter(models.FlatRate.flat_rate_name == flat_rate_name).all()
    if not flat_rates:
        return None
    flat_rate_base_values_list = []
    flat_rate_uptos_list = []
    flat_rate_increments_list = []
    flat_rate_value_of_increments_list = []
    rate_per_kw_hr_list = []
    for flat_rate in flat_rates:
        flat_rate_uptos_list.append(flat_rate.flat_rate_upto)
        flat_rate_base_values_list.append(flat_rate.flat_rate_base_value)
        rate_per_kw_hr_list.append(flat_rate.rate_per_kw_hr)
        flat_rate_increments = db.query(models.FlatRateIncrement).filter(models.FlatRateIncrement.flat_rate_id == flat_rate.flat_rate_id).all()
        for flat_rate_increment in flat_rate_increments:
            flat_rate_increments_list.append(flat_rate_increment.increment)
            flat_rate_value_of_increments_list.append(flat_rate_increment.value_of_increment)
        
        # flat_rate_increments_list.append(flat_rate_increments_list)
        # flat_rate_value_of_increments_list.append(flat_rate_value_of_increments_list)       
    
    return {
        "flat_rate_name": flat_rate_name,
        "flat_rate_base_value": flat_rate_base_values_list,
        "flat_rate_upto": flat_rate_uptos_list,
        "increment": flat_rate_increments_list,
        "value_of_increment": flat_rate_value_of_increments_list,
        "rate_per_kw_hr": rate_per_kw_hr_list,
    }


def get_flat_rates(db: Session, skip: int = 0, limit: int = 100):
    flat_rates = (
        db.query(models.FlatRate)
        .offset(skip)
        .limit(limit)
        .all()
    )
    unique_flat_rate_names = set()
    results = []

    for flat_rate in flat_rates:
        flat_rate_name = flat_rate.flat_rate_name
        if flat_rate_name not in unique_flat_rate_names:
            flat_rate_details = get_flat_rate(db, flat_rate_name)
            results.append(flat_rate_details)
            unique_flat_rate_names.add(flat_rate_name)

    return results

def create_flat_rate(db: Session, flat_rate: schemas.FlatRateCreate):
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_base_values = flat_rate.flat_rate_base_value
    flat_rate_uptos = flat_rate.flat_rate_upto
    increments = flat_rate.increment
    value_of_increments = flat_rate.value_of_increment
    rate_per_kw_hrs = flat_rate.rate_per_kw_hr
    if not (len(flat_rate_base_values) == len(flat_rate_uptos) == len(increments) == len(value_of_increments) == len(rate_per_kw_hrs)):
        return None
    flat_rate_ids = []
    for flat_rate_base_value, flat_rate_upto, rate_per_kw_hr in zip(flat_rate_base_values, flat_rate_uptos, rate_per_kw_hrs):
        db_flat_rate = models.FlatRate(flat_rate_name=flat_rate_name, flat_rate_base_value=flat_rate_base_value, flat_rate_upto=flat_rate_upto, rate_per_kw_hr=rate_per_kw_hr)
        db.add(db_flat_rate)
        db.flush()
        flat_rate_ids.append(db_flat_rate.flat_rate_id)
    i = 0
    for increment, value_of_increment in zip(increments, value_of_increments):
        db_flat_rate_increment = models.FlatRateIncrement(flat_rate_id=flat_rate_ids[i], increment=increment, value_of_increment=value_of_increment)
        db.add(db_flat_rate_increment)
        db.flush()
        i += 1
    db.commit()
    db.refresh(db_flat_rate)
    db.refresh(db_flat_rate_increment)
    return db_flat_rate
    # return db_flat_rate

def update_flat_rate(db: Session, flat_rate: schemas.FlatRateUpdate):
    # delete prev flat rate
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_ids = db.query(models.FlatRate.flat_rate_id).filter(models.FlatRate.flat_rate_name == flat_rate_name).all()
    
    flat_rate_ids = [flat_rate_id for (flat_rate_id,) in flat_rate_ids]
    
    for flat_rate_id in flat_rate_ids:
        db.query(models.FlatRateIncrement).filter(models.FlatRateIncrement.flat_rate_id == flat_rate_id).delete()
    db.query(models.FlatRate).filter(models.FlatRate.flat_rate_name == flat_rate_name).delete()
    
    # add new one
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_base_values = flat_rate.flat_rate_base_value
    flat_rate_uptos = flat_rate.flat_rate_upto
    increments = flat_rate.increment
    value_of_increments = flat_rate.value_of_increment
    rate_per_kw_hrs = flat_rate.rate_per_kw_hr
    if not (len(flat_rate_base_values) == len(flat_rate_uptos) == len(increments) == len(value_of_increments) == len(rate_per_kw_hrs)):
        return None
    flat_rate_ids = []
    for flat_rate_base_value, flat_rate_upto, rate_per_kw_hr in zip(flat_rate_base_values, flat_rate_uptos, rate_per_kw_hrs):
        db_flat_rate = models.FlatRate(flat_rate_name=flat_rate_name, flat_rate_base_value=flat_rate_base_value, flat_rate_upto=flat_rate_upto, rate_per_kw_hr=rate_per_kw_hr)
        db.add(db_flat_rate)
        db.flush()
        flat_rate_ids.append(db_flat_rate.flat_rate_id)
    i = 0
    for increment, value_of_increment in zip(increments, value_of_increments):
        db_flat_rate_increment = models.FlatRateIncrement(flat_rate_id=flat_rate_ids[i], increment=increment, value_of_increment=value_of_increment)
        db.add(db_flat_rate_increment)
        db.flush()
        i += 1
    db.commit()
    db.refresh(db_flat_rate)
    db.refresh(db_flat_rate_increment)
    return db_flat_rate


def delete_flat_rate(db: Session, flat_rate: schemas.FlatRateDelete):
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_ids = db.query(models.FlatRate.flat_rate_id).filter(models.FlatRate.flat_rate_name == flat_rate_name).all()
    
    flat_rate_ids = [flat_rate_id for (flat_rate_id,) in flat_rate_ids]
    
    for flat_rate_id in flat_rate_ids:
        db.query(models.FlatRateIncrement).filter(models.FlatRateIncrement.flat_rate_id == flat_rate_id).delete()
    db.query(models.FlatRate).filter(models.FlatRate.flat_rate_name == flat_rate_name).delete()
    db.commit()
    return 
# meter rate
def get_meter_rate(db: Session, meter_rate_name: str):
    mtr_rates = db.query(models.MeterRate).filter(models.MeterRate.meter_rate_name == meter_rate_name).all()
    if mtr_rates is None or len(mtr_rates) == 0:
        return None
    mtr_upto_list = []
    mtr_values_list = []
    for mtr_rate in mtr_rates:
        mtr_upto_list.append(mtr_rate.meter_rate_upto)
        mtr_values_list.append(mtr_rate.meter_rate_value)
    mtr_details = db.query(models.MeteredRateDetails).filter(models.MeteredRateDetails.meter_rate_name == meter_rate_name).first()
    electricity_duty = mtr_details.electricity_duty
    supply_type = mtr_details.supply_type
    rate_per_kw_hr = mtr_details.rate_per_kw_hr
    return {"meter_rate_name": meter_rate_name, "meter_rate_upto": mtr_upto_list, "meter_rate_value": mtr_values_list, "electricity_duty": electricity_duty, "supply_type": supply_type, "rate_per_kw_hr": rate_per_kw_hr}
    
    

def get_meter_rates(db: Session, skip: int = 0, limit: int = 100):
    mtr_details = db.query(models.MeteredRateDetails).offset(skip).limit(limit).all()
    result = []
    for mtr_detail in mtr_details:
        meter_rate_name = mtr_detail.meter_rate_name
        meter_rate_details = get_meter_rate(db, meter_rate_name)
        result.append(meter_rate_details)
    return result

def create_meter_rate(db: Session, meter_rate: schemas.MeterRateCreate):
    meter_rate_name = meter_rate.meter_rate_name
    meter_rate_values = meter_rate.meter_rate_value
    meter_rate_uptos = meter_rate.meter_rate_upto
    electricity_duty = meter_rate.electricity_duty
    supply_type = meter_rate.supply_type
    rate_per_kw_hr = meter_rate.rate_per_kw_hr
    
    for meter_rate_upto, meter_rate_value in zip(meter_rate_uptos, meter_rate_values):
        db_meter_rate = models.MeterRate(meter_rate_name=meter_rate_name, meter_rate_value=meter_rate_value, meter_rate_upto=meter_rate_upto)
        db.add(db_meter_rate)
        db.flush()
    db_metered_rate_details = models.MeteredRateDetails(meter_rate_name = meter_rate_name, electricity_duty = electricity_duty, supply_type = supply_type, rate_per_kw_hr = rate_per_kw_hr)
    db.add(db_metered_rate_details)
    db.flush()
    db.commit()
    db.refresh(db_meter_rate)
    db.refresh(db_metered_rate_details)
    return db_meter_rate

def update_meter_rate(db: Session, meter_rate: schemas.MeterRateUpdate):
    meter_rate_name = meter_rate.meter_rate_name
    meter_rate_values = meter_rate.meter_rate_value
    meter_rate_uptos = meter_rate.meter_rate_upto
    electricity_duty = meter_rate.electricity_duty
    supply_type = meter_rate.supply_type
    rate_per_kw_hr = meter_rate.rate_per_kw_hr

    # Delete old meter rate
    db.query(models.MeterRate).filter(models.MeterRate.meter_rate_name == meter_rate_name).delete()
    db.query(models.MeteredRateDetails).filter(models.MeteredRateDetails.meter_rate_name == meter_rate_name).delete()

    # Create new meter rate
    for meter_rate_upto, meter_rate_value in zip(meter_rate_uptos, meter_rate_values):
        db_meter_rate = models.MeterRate(
            meter_rate_name=meter_rate_name,
            meter_rate_value=meter_rate_value,
            meter_rate_upto=meter_rate_upto
        )
        db.add(db_meter_rate)
    db_metered_rate_details = models.MeteredRateDetails(
        meter_rate_name=meter_rate_name,
        electricity_duty=electricity_duty,
        supply_type=supply_type,
        rate_per_kw_hr=rate_per_kw_hr
    )
    db.add(db_metered_rate_details)
    db.commit()
    db.refresh(db_metered_rate_details)
    db.refresh(db_meter_rate)

    return db_metered_rate_details

def delete_meter_rate(db: Session, meter_rate: schemas.MeterRateDelete):
    # print(meter_rate['meter_rate_name'])
    
    meter_rate_name = meter_rate.meter_rate_name
    db.query(models.MeterRate).filter(models.MeterRate.meter_rate_name == meter_rate_name).delete()
    db.query(models.MeteredRateDetails).filter(models.MeteredRateDetails.meter_rate_name == meter_rate_name).delete()
    db.commit()
    return


# flat_rate_to_room

def get_flat_rate_to_room(db: Session, flat_rate_to_room_id: int):
    return db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.flat_rate_to_room_id == flat_rate_to_room_id).first()

def get_flat_rate_to_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FlatRateToRoom).offset(skip).limit(limit).all()

def create_flat_rate_to_room(db: Session, flat_rate_to_room: schemas.FlatRateToRoomCreate):
    flat_rate_id = flat_rate_to_room.flat_rate_id
    room_id = flat_rate_to_room.room_id
    db_flat_rate_to_room = models.FlatRateToRoom(flat_rate_id=flat_rate_id, room_id=room_id)
    db.add(db_flat_rate_to_room)
    db.commit()
    db.refresh(db_flat_rate_to_room)
    return db_flat_rate_to_room

def update_flat_rate_to_room(db: Session, flat_rate_to_room: schemas.FlatRateToRoomUpdate):
    flat_rate_to_room_id = flat_rate_to_room.flat_rate_to_room_id
    flat_rate_id = flat_rate_to_room.flat_rate_id
    room_id = flat_rate_to_room.room_id
    db_flat_rate_to_room = db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.flat_rate_to_room_id == flat_rate_to_room_id).first()
    db_flat_rate_to_room.flat_rate_id = flat_rate_id
    db_flat_rate_to_room.room_id = room_id
    db.commit()
    db.refresh(db_flat_rate_to_room)
    return db_flat_rate_to_room

def delete_flat_rate_to_room(db: Session, flat_rate_to_room: schemas.FlatRateToRoomDelete):
    flat_rate_to_room_id = flat_rate_to_room.flat_rate_to_room_id
    db_flat_rate_to_room = db.query(models.FlatRateToRoom).filter(models.FlatRateToRoom.flat_rate_to_room_id == flat_rate_to_room_id).first()
    db.delete(db_flat_rate_to_room)
    db.commit()
    return db_flat_rate_to_room

# meter_rate_to_room
def get_meter_rate_to_room(db: Session, meter_rate_to_room_id: int):
    return db.query(models.MeterRateToRoom).filter(models.MeterRateToRoom.meter_rate_to_room_id == meter_rate_to_room_id).first()

def get_meter_rate_to_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MeterRateToRoom).offset(skip).limit(limit).all()

def create_meter_rate_to_room(db: Session, meter_rate_to_room: schemas.MeterRateToRoomCreate):
    meter_rate_id = meter_rate_to_room.meter_rate_id
    room_id = meter_rate_to_room.room_id
    db_meter_rate_to_room = models.MeterRateToRoom(meter_rate_id=meter_rate_id, room_id=room_id)
    db.add(db_meter_rate_to_room)
    db.commit()
    db.refresh(db_meter_rate_to_room)
    return db_meter_rate_to_room

def update_meter_rate_to_room(db: Session, meter_rate_to_room: schemas.MeterRateToRoomUpdate):
    meter_rate_to_room_id = meter_rate_to_room.meter_rate_to_room_id
    meter_rate_id = meter_rate_to_room.meter_rate_id
    room_id = meter_rate_to_room.room_id
    db_meter_rate_to_room = db.query(models.MeterRateToRoom).filter(models.MeterRateToRoom.meter_rate_to_room_id == meter_rate_to_room_id).first()
    db_meter_rate_to_room.meter_rate_id = meter_rate_id
    db_meter_rate_to_room.room_id = room_id
    db.commit()
    db.refresh(db_meter_rate_to_room)
    return db_meter_rate_to_room


# reading
def get_reading(db: Session, reading_id: int):
    reading = db.query(models.Reading).filter(models.Reading.reading_id == reading_id).first()
    room_id = db.query(models.MeterToRoom.room_id).filter(models.MeterToRoom.meter_id == reading.meter_id).scalar()
    room_number = db.query(models.Room.room_number).filter(models.Room.room_id == room_id)
    quarter_id = db.query(models.Room.quarter_type_id).filter(models.Room.room_id == room_id)
    quarter_name = db.query(models.QuarterType.quarter_name).filter(models.QuarterType.quarter_id == quarter_id).scalar()
    return {
        "reading_id": reading.reading_id,
        "meter_id": reading.meter_id,
        "room_id": room_id,
        "room_number": room_number.scalar(),
        "quarter_type": quarter_name,
        "month": reading.month,
        "year": reading.year,
        "locked": reading.locked,
        "units_consumed": reading.units_consumed,
    }

    

def get_readings(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.Reading).offset(skip).limit(limit).all()
   try:
       readings = db.query(models.Reading).offset(skip).limit(limit).all()
       readings_list = []
       for reading in readings:
              room_id = db.query(models.MeterToRoom.room_id).filter(models.MeterToRoom.meter_id == reading.meter_id).scalar()
              room_number = db.query(models.Room.room_number).filter(models.Room.room_id == room_id)
              quarter_id = db.query(models.Room.quarter_type_id).filter(models.Room.room_id == room_id)
              quarter_name = db.query(models.QuarterType.quarter_name).filter(models.QuarterType.quarter_id == quarter_id).scalar()
              readings_list.append({
                "reading_id": reading.reading_id,
                "meter_id": reading.meter_id,
                "room_id": room_id,
                "room_number": room_number.scalar(),
                "quarter_type": quarter_name,
                "month": reading.month,
                "year": reading.year,
                "locked": reading.locked,
                "units_consumed": reading.units_consumed,
              })
       return readings_list
   except Exception as e:
        return None
    

def create_reading(db: Session, reading: schemas.ReadingCreate):
    meter_id = reading.meter_id
    month = reading.month
    year = reading.year
    prev_reading = (
        db.query(func.sum(models.Reading.units_consumed))
        .filter(models.Reading.meter_id == meter_id)
        .scalar() or 0
    )
    initial_reading = db.query(models.Meter.initial_reading).filter(models.Meter.meter_id == meter_id).scalar()
    prev_reading += initial_reading
    
    units_consumed = reading.units_consumed - prev_reading
    db_reading = models.Reading(meter_id=meter_id, month=month, year=year, units_consumed=units_consumed)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def update_reading(db: Session, reading: schemas.ReadingUpdate):
    reading_id = reading.reading_id
    meter_id = reading.meter_id
    month = reading.month
    year = reading.year
    prev_reading = (
        db.query(func.sum(models.Reading.units_consumed))
        .filter(models.Reading.meter_id == meter_id)
        .scalar() or 0
    )
    initial_reading = db.query(models.Meter.initial_reading).filter(models.Meter.id == meter_id).scalar()
    prev_reading += initial_reading
    
    units_consumed = reading.units_consumed - prev_reading
    db_reading = db.query(models.Reading).filter(models.Reading.reading_id == reading_id).first()
    db_reading.meter_id = meter_id
    db_reading.month = month
    db_reading.year = year
    db_reading.units_consumed = units_consumed
    db.commit()
    db.refresh(db_reading)
    return db_reading

def delete_reading(db: Session, reading: schemas.ReadingDelete):
    reading_id = reading.reading_id
    db_reading = db.query(models.Reading).filter(models.Reading.reading_id == reading_id).first()
    db.delete(db_reading)
    db.commit()
    return db_reading

def get_unmetered_bill(db: Session, bill_id: int):
    return db.query(models.UnmeteredBill).filter(models.UnmeteredBill.bill_id == bill_id).first()

def get_unmetered_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UnmeteredBill).offset(skip).limit(limit).all()

def create_unmetered_bill(db: Session, unmetered_bill: schemas.UnmeteredBillCreate):
    room_id = unmetered_bill.room_id
    month = unmetered_bill.month
    year = unmetered_bill.year
    user_to_room = db.query(models.UserToRoom).filter(models.UserToRoom.room_id == room_id).first()
    user_id = user_to_room.user_id
    # get flat rate
    flat_rate_id = db.query(models.FlatRateToRoom.flat_rate_id).filter(models.FlatRateToRoom.room_id == room_id).scalar()
    flat_rate = db.query(models.FlatRate.flat_rate_value).filter(models.FlatRate.flat_rate_id == flat_rate_id).scalar()
    db_bill = models.UnmeteredBill(room_id=room_id, user_id=user_id, month=month, year=year, amount=flat_rate)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

def delete_unmetered_bill(db: Session, bill: schemas.UnmeteredBillDelete):
    bill_id = bill.bill_id
    db_bill = db.query(models.UnmeteredBill).filter(models.UnmeteredBill.bill_id == bill_id).first()
    db.delete(db_bill)
    db.commit()
    return db_bill

# metered bill

def get_metered_bill(db: Session, bill_id: int):
    return db.query(models.MeteredBill).filter(models.MeteredBill.metered_bill_id == bill_id).first()

def get_metered_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MeteredBill).offset(skip).limit(limit).all()

def create_metered_bill(db: Session, metered_bill: schemas.MeteredBillCreate):
    meter_id = metered_bill.meter_id
    month = metered_bill.month
    year = metered_bill.year
    # get units consumed
    units_consumed = db.query(models.Reading.units_consumed).filter(models.Reading.meter_id == meter_id, models.Reading.year == year, models.Reading.month == month).scalar()
    # get meter rate
    room_id = db.query(models.MeterToRoom.room_id).filter(models.MeterToRoom.meter_id == meter_id).scalar()
    meter_rate_id = db.query(models.MeterRateToRoom.meter_rate_id).filter(models.MeterRateToRoom.room_id == room_id).scalar()
    
    meter_rate_name = db.query(models.MeterRate.meter_rate_name).filter(models.MeterRate.meter_rate_id == meter_rate_id).scalar()
    
    
    meter_rates = db.query(models.MeterRate.meter_rate_upto, models.MeterRate.meter_rate_value).filter(
    models.MeterRate.meter_rate_name == meter_rate_name).all()
    meter_rate_list = [(meter_rate.meter_rate_upto, meter_rate.meter_rate_value) for meter_rate in meter_rates]
    sorted_meter_rate_list = sorted(meter_rate_list, key=lambda x: x[0])
    
    bill_value = 0
    for val in sorted_meter_rate_list:
        if units_consumed <= val[0]:
            bill_value += units_consumed * val[1]
            break
        else:
            bill_value += val[0] * val[1]
            units_consumed -= val[0]
            
    user_id = db.query(models.UserToRoom.user_id).filter(models.UserToRoom.room_id == room_id).scalar()
    
    db_bill = models.MeteredBill(user_id = user_id, meter_id=meter_id, room_id = room_id, month=month, year=year, amount=bill_value)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def delete_metered_bill(db: Session, bill: schemas.MeteredBillDelete):
    bill_id = bill.metered_bill_id
    db_bill = db.query(models.MeteredBill).filter(models.MeteredBill.metered_bill_id == bill_id).first()
    db.delete(db_bill)
    db.commit()
    return db_bill


# bulk bill generation

def create_bulk_metered_bill(db: Session, metered_bill: schemas.BulkMeteredBillCreate):
    month = metered_bill.month
    year = metered_bill.year
    # get all metered rooms
    meterids = db.query(models.MeterToRoom.meter_id).all()
    db_bill_list = []
    for meterid in meterids:
        try:
            metered_bill_exists = db.query(models.MeteredBill).filter(models.MeteredBill.meter_id == meterid[0], models.MeteredBill.month == month, models.MeteredBill.year == year).first()
            if metered_bill_exists:
                continue
            db_bill = create_metered_bill(db, schemas.MeteredBillCreate(meter_id=meterid[0], month=month, year=year))
            db_bill_list.append(db_bill)
        except:
            continue
    return db_bill_list

def create_bulk_unmetered_bill(db: Session, unmetered_bill: schemas.BulkUnmeteredBillCreate):
    month = unmetered_bill.month
    year = unmetered_bill.year
    # get all unmetered rooms
    roomids = db.query(models.FlatRateToRoom.room_id).all()
    db_bill_list = []
    for roomid in roomids:
        try:
            unmetered_bill_exists = db.query(models.UnmeteredBill).filter(models.UnmeteredBill.room_id == roomid[0], models.UnmeteredBill.month == month, models.UnmeteredBill.year == year).first()
            if unmetered_bill_exists:
                continue
            db_bill = create_unmetered_bill(db, schemas.UnmeteredBillCreate(room_id=roomid[0], month=month, year=year))
            db_bill_list.append(db_bill)
        except:
            continue
    return db_bill_list

# FETCH REQUESTS : quarter_type , room_no ==> room_id
def get_room_id_from_room_no(db: Session, room_number: int, quarter_type_id: int):
    return db.query(models.Room.room_id, models.Room.is_metered).filter(models.Room.room_number == room_number, models.Room.quarter_type_id == quarter_type_id).all()

# FETCH REQUESTS : room_id ==> meter_id
def get_meter_id_from_room_id(db: Session, room_id: int):
    if db.query(models.Room.is_metered).filter(models.Room.room_id == room_id).scalar():
        meter = db.query(models.MeterToRoom.meter_id).filter(models.MeterToRoom.room_id == room_id).first()
        return meter.meter_id if meter else None
    else:
        return None