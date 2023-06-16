from pydantic import BaseModel, validator
from typing import Optional, List



# auth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# user
class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    user_id: int
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None
    disabled: bool = False
    access: str = 'user'

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    user_id: int
    username: str
    full_name: str | None = None
    disabled: bool = False
    access: str

    class Config:
        orm_mode = True


class UserDelete(BaseModel):
    user_id: int
    class Config:
        orm_mode = True

# Department
class DepartmentBase(BaseModel):
    department_name: str
    class Config:
        orm_mode = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    department_id: int

class DepartmentUpdate(DepartmentRead):
    pass

class DepartmentDelete(BaseModel):
    department_id: int
    class Config:
        orm_mode = True
# user to department
class UserToDepartmentBase(BaseModel):
    department_id: int
    user_id: int
    class Config:
        orm_mode = True
        
class UserToDepartmentCreate(UserToDepartmentBase):
    pass

class UserToDepartmentRead(UserToDepartmentBase):
    user_to_department_id: int
    
class UserToDepartmentUpdate(UserToDepartmentRead):
    pass

class UserToDepartmentDelete(BaseModel):
    user_to_department_id: int
    class Config:
        orm_mode = True

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

# Room Creation Metered

class RoomCreationBase(BaseModel):
    quarter_type_id: int
    room_number: int
    is_metered: bool

    class Config:
        orm_mode = True

class RoomCreationCreate(RoomCreationBase):
    initial_reading: Optional[int]
    meter_rate_id: Optional[int]
    flat_rate_id: Optional[int]
    

class RoomCreationRead(RoomCreationBase):
    room_id: int


class RoomCreationUpdate(RoomCreationBase):
    room_id: int

class RoomCreationDelete(BaseModel):
    room_id: int

    class Config:
        orm_mode = True
class RoomCreationReadMetered(RoomCreationBase):
    quarter_type_name: str
    # meter_id : int
    initial_reading: int
    meter_rate_name: str
    
class RoomCreationReadUnmetered(RoomCreationBase):
    flat_rate_name: str

# user creation
class UserCreationBase(BaseModel):
    username: str
    full_name: str | None = None
    class Config:
        orm_mode = True

class UserCreationCreate(UserCreationBase):
    password: str
    disabled: bool = False
    department_id: int
    room_id: int

class UserCreationRead(UserCreationBase):
    user_id: int
    disabled: bool = False
    
class UserCreationDelete(BaseModel):
    user_id: int
    class Config:
        orm_mode = True

# Flat Rate
class FlatRateBase(BaseModel):
    flat_rate_name: str

    class Config:
        orm_mode = True

class FlatRateCreate(BaseModel):
    flat_rate_name: str
    flat_rate_base_value: List[int]
    flat_rate_upto: List[int]
    increment: List[List[int]]
    value_of_increment: List[List[int]]
    rate_per_kw_hr: List[int]

    class Config:
        orm_mode = True

class FlatRateRead(BaseModel):
    flat_rate_name: str
    flat_rate_base_value: List[int]
    flat_rate_upto: List[int]
    increment: List[List[int]]
    value_of_increment: List[List[int]]
    rate_per_kw_hr: List[int]
    
    class Config:
        orm_mode = True

class FlatRateUpdate(FlatRateBase):
    flat_rate_name: str
    flat_rate_base_value: List[int]
    flat_rate_upto: List[int]
    increment: List[List[int]]
    value_of_increment: List[List[int]]
    rate_per_kw_hr: List[int]
    


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

class FlatRateToRoomRead(FlatRateToRoomCreate):
    pass

class FlatRateToRoomUpdate(FlatRateToRoomBase):
    flat_rate_id: int
    room_id: int

class FlatRateToRoomDelete(FlatRateToRoomBase):
    pass

# Meter Rate
class MeterRateBase(BaseModel):
    meter_rate_name:str

    class Config:
        orm_mode = True

class MeterRateCreate(BaseModel):
    meter_rate_name: str
    meter_rate_upto: List[int]
    meter_rate_value: List[int]
    electricity_duty: int
    supply_type: str
    rate_per_kw_hr: int
    @validator('supply_type')
    def validate_supply_type(cls, supply_type):
        valid_values = ['3-phase', 'single-phase']
        if supply_type not in valid_values:
            raise ValueError(f"Invalid supply_type value. Accepted values are: {', '.join(valid_values)}")
        return supply_type
    @validator('meter_rate_upto')
    def validate_meter_rate_upto(cls, meter_rate_upto, values):
        if 'meter_rate_value' in values and len(meter_rate_upto) != len(values['meter_rate_value']):
            raise ValueError("The 'meter_rate_upto' and 'meter_rate_value' lists must have equal lengths")
        return meter_rate_upto
    @validator('meter_rate_value')
    def validate_meter_rate_value(cls, meter_rate_value, values):
        if 'meter_rate_upto' in values and len(meter_rate_value) != len(values['meter_rate_upto']):
            raise ValueError("The 'meter_rate_upto' and 'meter_rate_value' lists must have equal lengths")
        return meter_rate_value
    class Config:
        orm_mode = True

class MeterRateRead(BaseModel):
    meter_rate_name: str
    meter_rate_upto: List[int]
    meter_rate_value: List[int]
    electricity_duty: int
    supply_type: str
    rate_per_kw_hr: int
    class Config:
        orm_mode = True

class MeterRateUpdate(BaseModel):
    meter_rate_name: str
    meter_rate_upto: List[int]
    meter_rate_value: List[int]
    electricity_duty: int
    supply_type: str
    rate_per_kw_hr: int
    class Config:
        orm_mode = True
    
    @validator('supply_type')
    def validate_supply_type(cls, supply_type):
        valid_values = ['3-phase', 'single-phase']
        if supply_type not in valid_values:
            raise ValueError(f"Invalid supply_type value. Accepted values are: {', '.join(valid_values)}")
        return supply_type
    @validator('meter_rate_upto')
    def validate_meter_rate_upto(cls, meter_rate_upto, values):
        if 'meter_rate_value' in values and len(meter_rate_upto) != len(values['meter_rate_value']):
            raise ValueError("The 'meter_rate_upto' and 'meter_rate_value' lists must have equal lengths")
        return meter_rate_upto
    @validator('meter_rate_value')
    def validate_meter_rate_value(cls, meter_rate_value, values):
        if 'meter_rate_upto' in values and len(meter_rate_value) != len(values['meter_rate_upto']):
            raise ValueError("The 'meter_rate_upto' and 'meter_rate_value' lists must have equal lengths")
        return meter_rate_value

class MeterRateDelete(MeterRateBase):
    pass

# Meter Rate To Room
class MeterRateToRoomBase(BaseModel):
    meter_rate_to_room_id: int
    class Config:
        orm_mode = True

class MeterRateToRoomCreate(BaseModel):
    meter_rate_id: int
    room_id: int
    class Config:
        orm_mode = True

class MeterRateToRoomRead(MeterRateToRoomCreate):
    pass

class MeterRateToRoomUpdate(MeterRateToRoomBase):
    meter_rate_id: int
    room_id: int

class MeterRateToRoomDelete(MeterRateToRoomBase):
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
    quarter_type: Optional[str]
    room_number: Optional[int]

class ReadingUpdate(ReadingBase,ReadingCreate):
    pass

class ReadingDelete(ReadingBase):
    pass


class UnmeteredBillBase(BaseModel):
    unmetered_bill_id: int
    class Config:
        orm_mode = True

class UnmeteredBillCreate(BaseModel):
    room_id: int
    month: int
    year: int
    
class UnmeteredBillRead(UnmeteredBillBase):
    room_id: int
    month: int
    year: int
    amount: int
    user_id: int

class UnmeteredBillUpdate(UnmeteredBillBase):
    month: int
    year: int
    amount: int

class UnmeteredBillDelete(UnmeteredBillBase):
    pass

#metered bill

class MeteredBillBase(BaseModel):
    metered_bill_id: int
    class Config:
        orm_mode = True

class MeteredBillCreate(BaseModel):
    meter_id: int
    month: int
    year: int
    
    class Config:
        orm_mode = True

class MeteredBillRead(MeteredBillBase):
    meter_id: int
    user_id: int
    room_id: int
    month: int
    year: int
    amount: int

class MeteredBillDelete(MeteredBillBase):
    pass

# bulk metered bill
class BulkMeteredBillCreate(BaseModel):
    month: int
    year: int
    class Config:
        orm_mode = True
        
class BulkUnmeteredBillCreate(BaseModel):
    month: int
    year: int
    class Config:
        orm_mode = True

# Quarter Type , Room No ==> RoomID       
class QuarterToRoomBase(BaseModel):
    room_number: int
    quarter_id: int
    class Config:
        orm_mode = True
        
class QuarterToRoomRead(QuarterToRoomBase):
    room_id: int
    is_metered: bool

      
# RoomID ==> MeterID
class RoomToMeterBase(BaseModel):
    room_id: int
    meter_id: int
    class Config:
        orm_mode = True

class RoomToMeterRead(RoomToMeterBase):
    pass