from typing import Annotated

from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from src.infrastructure.get_service import get_user_service
from src.application.services import UserService
from src.application.schemas import Token, UserReturnData
from src.application.token_type import TokenType
from src.application.auth_utils import AuthUtils

__all__ = [
    "login_router",
]


login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@login_router.post("/login")
async def login(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        user_service: UserService = Depends(get_user_service)
) -> Token:
    user = await user_service.get_user_by_username(username)
    if user is None or not AuthUtils.password_valid(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active"
        )

    return Token(
        access_token=AuthUtils.create_token(user, TokenType.ACCESS),
        refresh_token=AuthUtils.create_token(user, TokenType.REFRESH)
    )


@login_router.get("/me", response_model=UserReturnData)
async def get_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserService = Depends(get_user_service),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = AuthUtils.decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user
