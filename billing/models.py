from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from billing.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False, unique=True) # email
    hashed_password = Column(String)
    full_name = Column(String)
    access = Column(String(20), default='user')

    __table_args__ = (
        CheckConstraint(
            access.in_(['admin', 'operator', 'user']),
            name='access_check'
        ),
    )
    disabled = Column(Boolean, nullable=False, default=False)

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    department_name = Column(String, nullable=False, unique=True)


class Meter(Base):
    __tablename__ = "meters"

    meter_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    initial_reading = Column(Integer, nullable=False)


class QuarterType(Base):
    __tablename__ = "quarter_types"

    quarter_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    quarter_name = Column(String, nullable=False, unique=True)
    rooms = relationship("Room", cascade="all, delete", backref="quarter_type")
    # rooms = relationship("Room", back_populates="quarter_type", cascade="all, delete")


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    quarter_type_id = Column(Integer, ForeignKey("quarter_types.quarter_id", ondelete="CASCADE"), nullable=False)
    room_number = Column(Integer, nullable=False)
    is_metered = Column(Boolean, nullable=False)

    # quarter_type = relationship("QuarterType", back_populates="rooms", cascade="all, delete")

class UserToDepartment(Base):
    __tablename__ = "user_to_department"

    user_to_department_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)

class UserToRoom(Base):
    __tablename__ = "user_to_room"

    user_to_room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, unique=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False, unique=True)

    # user = relationship("User", back_populates="user_to_room")
    # room = relationship("Room", back_populates="user_to_room"


class MeterToRoom(Base):
    __tablename__ = "meter_to_room"

    meter_to_room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    meter_id = Column(Integer, ForeignKey("meters.meter_id"), nullable=False, unique=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False, unique=True)

    # meter = relationship("Meter", back_populates="meter_to_room")
    # room = relationship("Room", back_populates="meter_to_room")


class FlatRate(Base):
    __tablename__ = "flat_rates"

    flat_rate_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    flat_rate_name = Column(String, nullable=False, unique=True)
    flat_rate_value = Column(Integer, nullable=False)


class FlatRateToRoom(Base):
    __tablename__ = "flat_rate_to_room"

    flat_rate_to_room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    flat_rate_id = Column(Integer, ForeignKey("flat_rates.flat_rate_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False, unique=True)

    # flat_rate = relationship("FlatRate", back_populates="flat_rate_to_room")
    # room = relationship("Room", back_populates="flat_rate_to_room")


class MeterRate(Base):
    __tablename__ = "meter_rates"

    meter_rate_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    meter_rate_name = Column(String, nullable=False)
    meter_rate_upto = Column(Integer, nullable=False)
    meter_rate_value = Column(Integer, nullable=False)

class MeterRateToRoom(Base):
    __tablename__ = "meter_rate_to_room"

    meter_rate_to_room_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    meter_rate_id = Column(Integer, ForeignKey("meter_rates.meter_rate_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False, unique=True)

    # meter_rate = relationship("MeterRate", back_populates="meter_rate_to_room")
    # room = relationship("Room", back_populates="meter_rate_to_room")

class Reading(Base):
    __tablename__ = "readings"

    reading_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    meter_id = Column(Integer, ForeignKey("meters.meter_id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    units_consumed = Column(Integer, nullable=False)
    locked = Column(Boolean, default=False)
    __table_args__ = (
        CheckConstraint('month >= 1 AND month <= 12', name='check_month'),
        CheckConstraint('units_consumed >= 0', name='check_units_consumed'),
    )
    # meter = relationship("Meter", back_populates="readings")
    
class MeteredBill(Base):
    __tablename__ = "metered_bills"

    metered_bill_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    meter_id = Column(Integer, ForeignKey("meters.meter_id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('month >= 1 AND month <= 12', name='check_month'),
        CheckConstraint('year > 0', name='check_year'),
    )
    # user = relationship("User", back_populates="bills")
    # room = relationship("Room", back_populates="bills")

class UnmeteredBill(Base):
    __tablename__ = "unmetered_bills"

    unmetered_bill_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('month >= 1 AND month <= 12', name='check_month'),
        CheckConstraint('year > 0', name='check_year'),
    )