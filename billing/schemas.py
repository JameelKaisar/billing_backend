from pydantic import BaseModel


class MeterBase(BaseModel):
    initial_reading: int


class MeterCreate(MeterBase):
    pass


class Meter(MeterBase):
    meter_id: int

    class Config:
        orm_mode = True
