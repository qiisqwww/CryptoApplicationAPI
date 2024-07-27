from datetime import timedelta
from typing import Annotated

from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.config import TOKEN_LIFETIME
from src.auth.services import UserService, get_user_service
from src.auth.schemas import Token, TokenData
from src.auth.utils import create_access_token, get_password_hash

__all__ = [
    "login_router",
]


login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")


@login_router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(get_user_service)
) -> Token:
    user = await user_service.check_user_exists(form_data.username, get_password_hash(form_data.password))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(seconds=TOKEN_LIFETIME)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
