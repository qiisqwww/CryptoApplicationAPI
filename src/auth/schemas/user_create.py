from typing import Optional

from pydantic import BaseModel

__all__ = [
    "UserCreate"
]


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
