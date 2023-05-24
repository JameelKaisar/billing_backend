from pydantic import BaseModel


class MeterBase(BaseModel):
    initial_reading: int


class MeterCreate(MeterBase):
    pass


class Meter(MeterBase):
    meter_id: int

# Flat Rate
class FlatRateBase(BaseModel):
    flat_rate_id:int

class FlatRateCreate(BaseModel):
    flat_rate_name: str
    flat_rate_value: int

class FlatRateRead(FlatRateBase):
    pass

class FlatRateUpdate(FlatRateBase):
    flat_rate_name: str
    flat_rate_value: int

class FaltRateDelete(FlatRateBase):
    pass

# Flat Rate To Room
class FlatRateToRoomBase(BaseModel):
    flat_rate_to_room_id: int


class FlatRateToRoomCreate(BaseModel):
    flat_rate_id: int
    room_id: int

class FlatRateToRoomRead(FlatRateToRoomBase):
    pass

class FlatRateToRoomUpdate(FlatRateToRoomBase):
    flat_rate_id: int
    room_id: int

class FlatRateToRoomDelete(FlatRateToRoomBase):
    pass

# Meter Rate
class MeterRateBase(BaseModel):
    meter_rate_id:int

class MeterRateCreate(BaseModel):
    meter_rate_name: str
    meter_rate_upto: int
    meter_rate_value: int

class MeterRateRead(MeterRateBase):
    pass

class MeterRateUpdate(MeterRateBase):
    meter_rate_name: str
    meter_rate_upto: int
    meter_rate_value: int

class MeterRateDelete(MeterRateBase):
    pass

# Reading
class ReadingBase(BaseModel):
    reading_id: int
    

class ReadingCreate(BaseModel):
    meter_id: int
    month: int
    year: int
    units_consumed: int

class ReadingRead(ReadingBase):
    locked: bool

class ReadingUpdate(ReadingBase,ReadingCreate):
    pass

class ReadingDelete(ReadingBase):
    pass

















    




    




    class Config:
        orm_mode = True
