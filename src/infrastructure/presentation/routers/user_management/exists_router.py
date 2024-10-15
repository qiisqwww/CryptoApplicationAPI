from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.infrastructure.get_service import get_user_service
from src.application.services import UserService

__all__ = [
    "exists_router"
]


exists_router = APIRouter()


@exists_router.get("/exists")
async def find_user_exists(
        user_id: Annotated[int, Query()],
        user_service: UserService = Depends(get_user_service)
) -> dict:
    user_exists = await user_service.user_exists(user_id)
    return {"user_exists": user_exists}
