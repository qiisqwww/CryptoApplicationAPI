from datetime import timedelta, datetime, timezone

from jwt import encode, decode
from bcrypt import hashpw, checkpw, gensalt

from src.application.schemas import UserData
from src.application.token_type import TokenType
from src.config import (
    ALGORITHM,
    PRIVATE_KEY_PATH,
    PUBLIC_KEY_PATH,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


_all__ = [
    "AuthUtils"
]


class AuthUtils:
    @staticmethod
    def create_token(user: UserData, token_type: TokenType, private_key: str = PRIVATE_KEY_PATH.read_text()) -> str:
        expire = datetime.now(timezone.utc) + AuthUtils._get_timedelta_for_token(token_type)

        user_payload = {
            TokenType.FIELD: token_type,
            "sub": user.username,
            "email": user.email,
            "exp": expire
        }

        access_token = encode(user_payload, private_key, algorithm=ALGORITHM)
        return access_token

    @staticmethod
    def _get_timedelta_for_token(token_type: TokenType) -> timedelta:
        match token_type:
            case TokenType.ACCESS:
                return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            case TokenType.REFRESH:
                return timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            case _:
                return timedelta(0)

    @staticmethod
    def decode_token(token: str | bytes, public_key: str = PUBLIC_KEY_PATH.read_text()) -> dict:
        decoded_jwt = decode(token, public_key, algorithms=[ALGORITHM])
        return decoded_jwt

    @staticmethod
    def hashed_password(password: str) -> str:
        salt = gensalt()
        return str(hashpw(password.encode(), salt).decode("utf-8"))  # TODO: разобраться с хранением пароля в bytes

    @staticmethod
    def password_valid(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
