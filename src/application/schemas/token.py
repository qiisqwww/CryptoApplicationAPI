from pydantic import BaseModel

__all__ = [
    "Token"
]


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
