from typing import Annotated

from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infrastructure.get_service import get_user_service
from src.application.services import UserService
from src.application.schemas import Token
from src.application.token_type import TokenType
from src.application.auth_utils import AuthUtils

__all__ = [
    "refresh_token_router"
]


refresh_token_router = APIRouter()
http_bearer = HTTPBearer()


@refresh_token_router.post(
    "/refresh",
    response_model=Token,
    response_model_exclude_none=True
)
async def refresh_access_token(
        token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],  # TODO: возможно стоит ждать str
        user_service: UserService = Depends(get_user_service),
) -> Token:
    try:
        payload = AuthUtils.decode_token(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_type = payload.get(TokenType.FIELD)
    if token_type != TokenType.REFRESH:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"expected '{TokenType.REFRESH}', found {token_type!r} token type",
            headers={"WWW-Authenticate": "Bearer    "},
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

    return Token(access_token=AuthUtils.create_token(user, TokenType.ACCESS))
