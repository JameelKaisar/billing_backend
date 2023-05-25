from sqlalchemy.orm import Session

from billing import models, schemas

#user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_users(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    user_id = user.user_id
    user_name = user.user_name
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user.user_name = user_name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: schemas.UserDelete):
    user_id = user.user_id
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

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

#flat rate
def get_flat_rate(db: Session, flat_rate_id: int):
    return db.query(models.FlatRate).filter(models.FlatRate.flat_rate_id == flat_rate_id).first()

def get_flat_rates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FlatRate).offset(skip).limit(limit).all()

def create_flat_rate(db: Session, flat_rate: schemas.FlatRateCreate):
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_value = flat_rate.flat_rate_value
    db_flat_rate = models.FlatRate(flat_rate_name=flat_rate_name, flat_rate_value=flat_rate_value)
    db.add(db_flat_rate)
    db.commit()
    db.refresh(db_flat_rate)
    return db_flat_rate

def update_flat_rate(db: Session, flat_rate: schemas.FlatRateUpdate):
    flat_rate_id = flat_rate.flat_rate_id
    flat_rate_name = flat_rate.flat_rate_name
    flat_rate_value = flat_rate.flat_rate_value
    db_flat_rate = db.query(models.FlatRate).filter(models.FlatRate.flat_rate_id == flat_rate_id).first()
    db_flat_rate.flat_rate_name = flat_rate_name
    db_flat_rate.flat_rate_value = flat_rate_value
    db.commit()
    db.refresh(db_flat_rate)
    return db_flat_rate

def delete_flat_rate(db: Session, flat_rate: schemas.FlatRateDelete):
    flat_rate_id = flat_rate.flat_rate_id
    db_flat_rate = db.query(models.FlatRate).filter(models.FlatRate.flat_rate_id == flat_rate_id).first()
    db.delete(db_flat_rate)
    db.commit()
    return db_flat_rate

# meter rate
def get_meter_rate(db: Session, meter_rate_id: int):
    return db.query(models.MeterRate).filter(models.MeterRate.meter_rate_id == meter_rate_id).first()

def get_meter_rates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MeterRate).offset(skip).limit(limit).all()

def create_meter_rate(db: Session, meter_rate: schemas.MeterRateCreate):
    meter_rate_name = meter_rate.meter_rate_name
    meter_rate_value = meter_rate.meter_rate_value
    meter_rate_upto = meter_rate.meter_rate_upto
    db_meter_rate = models.MeterRate(meter_rate_name=meter_rate_name, meter_rate_value=meter_rate_value, meter_rate_upto=meter_rate_upto)
    db.add(db_meter_rate)
    db.commit()
    db.refresh(db_meter_rate)
    return db_meter_rate

def update_meter_rate(db: Session, meter_rate: schemas.MeterRateUpdate):
    meter_rate_id = meter_rate.meter_rate_id
    meter_rate_name = meter_rate.meter_rate_name
    meter_rate_value = meter_rate.meter_rate_value
    db_meter_rate = db.query(models.MeterRate).filter(models.MeterRate.meter_rate_id == meter_rate_id).first()
    db_meter_rate.meter_rate_name = meter_rate_name
    db_meter_rate.meter_rate_value = meter_rate_value
    db.commit()
    db.refresh(db_meter_rate)
    return db_meter_rate

def delete_meter_rate(db: Session, meter_rate: schemas.MeterRateDelete):
    meter_rate_id = meter_rate.meter_rate_id
    db_meter_rate = db.query(models.MeterRate).filter(models.MeterRate.meter_rate_id == meter_rate_id).first()
    db.delete(db_meter_rate)
    db.commit()
    return db_meter_rate


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

# reading
def get_reading(db: Session, reading_id: int):
    return db.query(models.Reading).filter(models.Reading.reading_id == reading_id).first()

def get_readings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reading).offset(skip).limit(limit).all()

def create_reading(db: Session, reading: schemas.ReadingCreate):
    meter_id = reading.meter_id
    month = reading.month
    year = reading.year
    units_consumed = reading.units_consumed
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
    units_consumed = reading.units_consumed
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

# bill

def get_bill(db: Session, bill_id: int):
    return db.query(models.Bill).filter(models.Bill.bill_id == bill_id).first()

def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()

def create_bill(db: Session, bill: schemas.BillCreate):
    bill_name = bill.bill_name
    bill_value = bill.bill_value
    bill_upto = bill.bill_upto
    db_bill = models.Bill(bill_name=bill_name, bill_value=bill_value, bill_upto=bill_upto)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill

def delete_bill(db: Session, bill: schemas.BillDelete):
    bill_id = bill.bill_id
    db_bill = db.query(models.Bill).filter(models.Bill.bill_id == bill_id).first()
    db.delete(db_bill)
    db.commit()
    return db_bill
