from datetime import timedelta, datetime, timezone

from jwt import encode, decode
from bcrypt import hashpw, checkpw, gensalt

from src.config import (
    ALGORITHM,
    PRIVATE_KEY_PATH,
    PUBLIC_KEY_PATH,
    TOKEN_LIFETIME
)


_all__ = [
    "AuthUtils"
]


class AuthUtils:
    @staticmethod
    def encoded_jwt(data: dict, private_key: str = PRIVATE_KEY_PATH.read_text()) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_LIFETIME)
        to_encode.update({"exp": expire})

        encoded_jwt = encode(to_encode, private_key, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decoded_jwt(token: str | bytes, public_key: str = PUBLIC_KEY_PATH.read_text()) -> dict:
        decoded_jwt = decode(token, public_key, algorithms=[ALGORITHM])
        return decoded_jwt

    @staticmethod
    def hashed_password(password: str) -> str:
        salt = gensalt()
        return str(hashpw(password.encode(), salt).decode("utf-8"))  # TODO: разобраться с хранением пароля в bytes

    @staticmethod
    def password_valid(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
