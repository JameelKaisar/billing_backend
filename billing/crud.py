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
