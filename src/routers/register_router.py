from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas import UserInputData, UserReturnData
from src.services import UserService, get_user_service
from src.utils import get_hashed_password

__all__ = [
    "register_router",
]


register_router = APIRouter()


@register_router.post("/register", response_model=UserReturnData)
async def register_user(user: UserInputData, user_service: UserService = Depends(get_user_service)):
    user_username_exists = await user_service.get_user_by_username(user.username)
    if user_username_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this username already exists"
        )

    user_email_exists = await user_service.get_user_by_email(user.email)
    if user_email_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this email already exists"
        )

    hashed_password = get_hashed_password(user.password)
    registered_user = await user_service.register_user(user, hashed_password)
    return registered_user