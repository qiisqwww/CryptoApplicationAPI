from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from src.infrastructure.get_service import get_user_service
from src.application.schemas import UserReturnData
from src.application.auth_utils import AuthUtils
from src.application.token_type import TokenType
from src.application.services import UserService

__all__ = [
    "get_me_router"
]


get_me_router = APIRouter()
http_bearer = HTTPBearer()


@get_me_router.get("/me", response_model=UserReturnData)
async def get_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        user_service: UserService = Depends(get_user_service),
):
    try:
        payload = AuthUtils.decode_token(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_type = payload.get(TokenType.FIELD)
    if token_type != TokenType.ACCESS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"expected '{TokenType.ACCESS}', found {token_type!r} token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
