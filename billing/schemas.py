from pydantic import BaseModel

#user

class UserBase(BaseModel):
    user_id: int
    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    user_name: str
    class Config:
        orm_mode = True
class UserRead(UserBase):
    user_name: str

class UserUpdate(UserBase):
    user_name: str
    
class UserDelete(UserBase):
    pass

# meter
class MeterBase(BaseModel):
    initial_reading: int
    class Config:
        orm_mode = True

class MeterCreate(MeterBase):
    pass
class MeterRead(MeterBase):
    meter_id: int

class MeterUpdate(MeterBase):
    meter_id: int

class MeterDelete(BaseModel):
    meter_id: int
    class Config:
        orm_mode = True

# quarter type
class QuarterTypeBase(BaseModel):
    quarter_name: str
    class Config:
        orm_mode = True

class QuarterTypeCreate(QuarterTypeBase):
    pass

class QuarterTypeRead(QuarterTypeBase):
    quarter_id: int

class QuarterTypeUpdate(QuarterTypeRead):
    pass

class QuarterTypeDelete(BaseModel):
    quarter_id: int
    class Config:
        orm_mode = True

# room

class RoomBase(BaseModel):
    room_number: int
    quarter_type_id: int
    class Config:
        orm_mode = True 
class RoomCreate(RoomBase):
    is_metered: bool

class RoomRead(RoomCreate):
    room_id: int

class RoomUpdate(RoomCreate):
    room_id: int

class RoomDelete(BaseModel):
    room_id: int
    class Config:
        orm_mode = True 


#user to room
class UserToRoomBase(BaseModel):
    user_id: int
    room_id: int
    class Config:
        orm_mode = True

class UserToRoomCreate(UserToRoomBase):
    pass

class UserToRoomRead(UserToRoomBase):
    user_to_room_id: int

    class Config:
        orm_mode = True

class UserToRoomUpdate(UserToRoomBase):
    user_to_room_id: int

class UserToRoomDelete(BaseModel):
    user_to_room_id: int

    class Config:
        orm_mode = True

# meter to room
class MeterToRoomBase(BaseModel):
    meter_id: int
    room_id: int

    class Config:
        orm_mode = True

class MeterToRoomCreate(MeterToRoomBase):
    pass

class MeterToRoomRead(MeterToRoomBase):
    meter_to_room_id: int

class MeterToRoomUpdate(MeterToRoomRead):
    pass

class MeterToRoomDelete(BaseModel):
    meter_to_room_id: int

    class Config:
        orm_mode = True

# Flat Rate
class FlatRateBase(BaseModel):
    flat_rate_id:int

    class Config:
        orm_mode = True

class FlatRateCreate(BaseModel):
    flat_rate_name: str
    flat_rate_value: int

    class Config:
        orm_mode = True

class FlatRateRead(FlatRateBase):
    flat_rate_name: str
    flat_rate_value: int

class FlatRateUpdate(FlatRateBase):
    flat_rate_name: str
    flat_rate_value: int

class FlatRateDelete(FlatRateBase):
    pass

# Flat Rate To Room
class FlatRateToRoomBase(BaseModel):
    flat_rate_to_room_id: int
    class Config:
        orm_mode = True


class FlatRateToRoomCreate(BaseModel):
    flat_rate_id: int
    room_id: int
    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

class MeterRateCreate(BaseModel):
    meter_rate_name: str
    meter_rate_upto: int
    meter_rate_value: int

    class Config:
        orm_mode = True

class MeterRateRead(MeterRateBase):
    meter_rate_name: str
    meter_rate_upto: int
    meter_rate_value: int

class MeterRateUpdate(MeterRateRead):
    meter_rate_name: str
    meter_rate_upto: int
    meter_rate_value: int

class MeterRateDelete(MeterRateBase):
    pass

# Reading
class ReadingBase(BaseModel):
    reading_id: int
    class Config:
        orm_mode = True

class ReadingCreate(BaseModel):
    meter_id: int
    month: int
    year: int
    units_consumed: int
    class Config:
        orm_mode = True
class ReadingRead(ReadingBase):
    meter_id: int
    month: int
    year: int
    units_consumed: int
    locked: bool

class ReadingUpdate(ReadingBase,ReadingCreate):
    pass

class ReadingDelete(ReadingBase):
    pass

#bill
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


