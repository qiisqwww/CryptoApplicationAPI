from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form

from src.infrastructure.get_service import get_auth_service
from src.application.services import (
    AuthService,
    UserWasNotFoundException,
    UserIsNotActiveException
)
from src.application.schemas import Token

__all__ = [
    "login_router",
]


login_router = APIRouter()


@login_router.post("/login")
async def login(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    try:
        token = await auth_service.authenticate(username, password)
    except UserWasNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserIsNotActiveException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active"
        ) from e

    return token
