from datetime import timedelta
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.config import TOKEN_LIFETIME, SECRET, ALGORITHM
from src.auth.services import UserService, get_user_service
from src.auth.schemas import Token, TokenData, UserReturnData
from src.auth.utils import create_access_token

__all__ = [
    "login_router",
]


login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@login_router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(get_user_service)
) -> Token:
    user = await user_service.get_user_by_username(form_data.username)
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


# @login_router.get("/me", response_model=UserReturnData)
# async def get_user(
#         token: Annotated[str, Depends(oauth2_scheme)],
#         user_service: UserService = Depends(get_user_service),
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#
#     user = await user_service.get_user_by_username(token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
