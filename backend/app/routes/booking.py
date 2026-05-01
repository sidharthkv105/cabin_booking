from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, time

from app.db import get_db
from app.models import Booking
from pydantic import BaseModel
from app.auth import get_current_user

router = APIRouter(prefix="/booking")

# sample cabins
CABINS = [
    {"id": 1, "name": "Cabin A"},
    {"id": 2, "name": "Cabin B"},
    {"id": 3, "name": "Cabin C"},
    {"id": 4, "name": "Cabin D"},
]

@router.get("/availability")
def check_availability(date: date, from_time: time, to_time: time, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.date == date).all()

    result = []

    for cabin in CABINS:
        is_booked = False

        for b in bookings:
            if b.cabin_id == cabin["id"]:
                # overlap check
                if not (to_time <= b.start_time or from_time >= b.end_time):
                    is_booked = True

        result.append({
            "id": cabin["id"],
            "name": cabin["name"],
            "booked": is_booked
        })

    return result

class BookingRequest(BaseModel):
    cabin_id: int
    date: date
    from_time: time
    to_time: time

@router.post("/")
def create_booking(
    data: BookingRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    booking = Booking(
        user_id=user["user_id"],   # ✅ dynamic
        cabin_id=data.cabin_id,
        date=data.date,
        start_time=data.from_time,
        end_time=data.to_time
    )

    db.add(booking)
    db.commit()

    return {"message": "Booking successful"}

@router.get("/my")
def get_my_bookings(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == user["user_id"]
    ).all()

    return bookings

@router.delete("/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return {"error": "Not found"}

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled"}