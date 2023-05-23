from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from billing.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class Meter(Base):
    __tablename__ = "meters"

    meter_id = Column(Integer, primary_key=True,
                      autoincrement=True, index=True)
    initial_reading = Column(Integer, nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)


class QuaterType(Base):
    __tablename__ = "quater_types"

    quater_id = Column(Integer, primary_key=True,
                       autoincrement=True, index=True)
    quater_name = Column(String, nullable=False)
    rooms = relationship("Room", back_populates="quater_type")


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    room_number = Column(Integer, nullable=False)
    quater_type_id = Column(Integer, ForeignKey(
        "QuartarType.quarter_id"), nullable=False)
    quater_type = relationship("QuaterType", back_populates="rooms")
    is_metered = Column(Boolean, nullable=False)


class UserToRoom(Base):
    __tablename__ = "user_to_room"

    user_to_room_id = Column(Integer, primary_key=True,
                             autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)
    # user = relationship("User", back_populates="user_to_room")
    # room = relationship("Room", back_populates="user_to_room"


class MeterToRoom(Base):
    __tablename__ = "meter_to_room"

    meter_to_room_id = Column(
        Integer, primary_key=True, autoincrement=True, index=True)
    meter_id = Column(Integer, ForeignKey("Meter.meter_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)
    # meter = relationship("Meter", back_populates="meter_to_room")
    # room = relationship("Room", back_populates="meter_to_room")


class FlatRate(Base):
    __tablename__ = "flat_rates"

    flat_rate_id = Column(Integer, primary_key=True,
                          autoincrement=True, index=True)
    flat_rate = Column(Integer, nullable=False)


class FlatRateToRoom(Base):
    __tablename__ = "flat_rate_to_room"

    flat_rate_to_room_id = Column(
        Integer, primary_key=True, autoincrement=True, index=True)
    flat_rate_id = Column(Integer, ForeignKey(
        "FlatRate.flat_rate_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)
    # flat_rate = relationship("FlatRate", back_populates="flat_rate_to_room")
    # room = relationship("Room", back_populates="flat_rate_to_room")


class MeterRate(Base):
    __tablename__ = "meter_rates"

    meter_rate_id = Column(Integer, primary_key=True,
                           autoincrement=True, index=True)
    upto = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)


class Reading(Base):
    __tablename__ = "readings"

    reading_id = Column(Integer, primary_key=True,
                        autoincrement=True, index=True)
    meter_id = Column(Integer, ForeignKey("Meter.meter_id"), nullable=False)
    units_consumed = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    locked = Column(Boolean, default=False)
    # meter = relationship("Meter", back_populates="readings")


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    # user = relationship("User", back_populates="bills")
    # room = relationship("Room", back_populates="bills")
