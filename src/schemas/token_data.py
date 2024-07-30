from pydantic import BaseModel

__all__ = [
    "TokenData"
]


class TokenData(BaseModel):
    username: str | None = None
