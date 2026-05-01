from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ SIGNUP
@router.post("/signup")
def signup(data: dict, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == data["username"]).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=data["username"],
        password=hash_password(data["password"])
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


# ✅ LOGIN (already exists)
@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data["username"]).first()

    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
    "user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}