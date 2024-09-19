from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructure import get_async_session
from src.infrastructure.repositories import UserRepository
from src.application.services import UserService

__all__ = [
    "get_user_service",
]


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(UserRepository(session=session))
