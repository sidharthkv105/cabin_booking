from sqlalchemy import Column, Integer, String, Date, Time
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)   # ✅ ADD THIS
    cabin_id = Column(Integer)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)