from typing import Optional

from fastapi_users.schemas import BaseUser

__all__ = [
    "UserRead"
]


class UserRead(BaseUser[int]):
    id: int
    username: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
