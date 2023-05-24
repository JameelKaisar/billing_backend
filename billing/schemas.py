from pydantic import BaseModel


class MeterBase(BaseModel):
    initial_reading: int

class MeterCreate(MeterBase):
    pass

class MeterRead(MeterBase):
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

class MeterUpdate(MeterBase):
    meter_id: int

class MeterDelete(MeterUpdate):
    pass


class QuarterTypeBase(BaseModel):
    quarter_name: str

class QuarterTypeCreate(QuarterTypeBase):
    quarter_id: int

class QuarterTypeRead(QuarterTypeCreate):
    
    class Config:
        orm_mode = True

class QuarterTypeUpdate(QuarterTypeCreate):
    pass

class QuarterTypeDelete(QuarterTypeCreate):
    pass


class RoomBase(BaseModel):
    room_number: int
    quarter_type_id: int

class RoomCreate(RoomBase):
    is_metered: bool

class RoomRead(RoomBase):
    room_id: int

    class Config:
        orm_mode = True 

class RoomUpdate(RoomCreate):
    room_id: int

class RoomDelete(RoomUpdate):
    pass


class UserToRoomBase(BaseModel):
    user_id: int
    room_id: int

class UserToRoomCreate(UserToRoomBase):
    pass

class UserToRoomRead(UserToRoomBase):
    user_to_room_id: int

    class Config:
        orm_mode = True

class UserToRoomUpdate(UserToRoomBase):
    user_to_room_id: int

class UserToRoomDelete(UserToRoomUpdate):
    pass


class MeterToRoomBase(BaseModel):
    meter_id: int
    room_id: int

class MeterToRoomCreate(MeterToRoomBase):
    pass

class MeterToRoomRead(MeterToRoomBase):
    meter_to_room_id: int

    class Config:
        orm_mode = True

class MeterToRoomUpdate(BaseModel):
    meter_to_room_id: int

class MeterToRoomDelete(MeterToRoomUpdate):
    pass


class BillBase(BaseModel):
    user_id: int
    room_id: int
    meter_id: int

class BillCreate(BillBase):
    month: int
    year: int
    amount: int
    
# Bill cannot be updated 

class BillRead(BillCreate):
    bill_id: int

    class Config:
        orm_mode = True

class BillDelete(BillCreate):
    bill_id: int

