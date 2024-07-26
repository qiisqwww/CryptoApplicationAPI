from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.config import SECRET
from src.auth.models import User
from src.auth.dependencies import get_user_db

__all__ = [
    "UserManager",
    "get_user_manager"
]


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
