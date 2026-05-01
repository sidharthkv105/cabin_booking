from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# 🔐 Config
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔑 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 OAuth2 scheme (used for extracting token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ---------------- PASSWORD ----------------

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ---------------- TOKEN ----------------

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- CURRENT USER ----------------

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"user_id": user_id}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")