from typing import Optional

from fastapi_users.schemas import BaseUserUpdate

__all__ = [
    "UserUpdate"
]


class UserUpdate(BaseUserUpdate):
    username: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
