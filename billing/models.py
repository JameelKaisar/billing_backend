from sqlalchemy import Column, Integer

from billing.database import Base


class Meter(Base):
    __tablename__ = "meters"

    meter_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    initial_reading = Column(Integer, nullable=False)
