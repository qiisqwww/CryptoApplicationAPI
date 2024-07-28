from datetime import timedelta, datetime, timezone

import jwt
from passlib.context import CryptContext

from src.config import SECRET, ALGORITHM


_all__ = [
    "create_access_token",
    "verify_password",
    "get_password_hash",
]


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)
