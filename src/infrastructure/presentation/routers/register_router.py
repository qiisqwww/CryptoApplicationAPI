from fastapi import APIRouter, Depends, HTTPException, status

from src.infrastructure.get_service import get_user_service
from src.application.services import (
    UserService,
    UsernameAlreadyUsedException,
    EmailAlreadyUsedException,
)
from src.application.schemas import UserInputData, UserReturnData

__all__ = [
    "register_router",
]


register_router = APIRouter()


@register_router.post("/register", response_model=UserReturnData)
async def register_user(
        user: UserInputData,
        user_service: UserService = Depends(get_user_service)
):
    try:
        registered_user = await user_service.register(user)
    except UsernameAlreadyUsedException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this username already exists"
        ) from e
    except EmailAlreadyUsedException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this email already exists"
        ) from e

    return registered_user
