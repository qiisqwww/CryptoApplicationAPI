from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from src.infrastructure.get_service import get_auth_service
from src.application.schemas import UserReturnData
from src.application.token_type import TokenType
from src.application.services import (
    AuthService,
    UnexpectedTokenTypeException,
    UserWasNotFoundException
)

__all__ = [
    "get_me_router"
]


get_me_router = APIRouter()
http_bearer = HTTPBearer()


@get_me_router.get("/me", response_model=UserReturnData)
async def get_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth_service.authorize(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UnexpectedTokenTypeException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"expected only '{TokenType.ACCESS}' token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserWasNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
