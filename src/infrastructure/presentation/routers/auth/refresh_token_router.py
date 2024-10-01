from typing import Annotated

from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infrastructure.get_service import get_auth_service
from src.application.services import (
    AuthService,
    UserWasNotFoundException,
    UnexpectedTokenTypeException
)
from src.application.schemas import Token
from src.application.token_type import TokenType

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
        auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    try:
        token = await auth_service.refresh_access_token(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UnexpectedTokenTypeException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"expected only '{TokenType.REFRESH}' token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserWasNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
