from typing import Annotated

from fastapi import APIRouter, Depends, Query, Header, HTTPException, status

from src.infrastructure.get_service import get_user_service
from src.application.services import UserService
from src.config import SECRET_INSIDE_KEY

__all__ = [
    "exists_router"
]


exists_router = APIRouter()


@exists_router.get("/exists")
async def find_user_exists(
        user_id: Annotated[int, Query()],
        secret_inside_key: Annotated[str, Header()],
        user_service: UserService = Depends(get_user_service)
) -> dict:
    if secret_inside_key != SECRET_INSIDE_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Invalid secret-inside-key."
        )

    user_exists = await user_service.user_exists(user_id)
    return {'user_exists': user_exists}
