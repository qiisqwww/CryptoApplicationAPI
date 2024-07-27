from typing import Optional

from pydantic import BaseModel

__all__ = [
    "UserRead"
]


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
