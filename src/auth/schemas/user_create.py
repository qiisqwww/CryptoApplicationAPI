from typing import Optional

from fastapi_users.schemas import BaseUserCreate

__all__ = [
    "UserCreate"
]


class UserCreate(BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
