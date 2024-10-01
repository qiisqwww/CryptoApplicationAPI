from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructure.database import get_async_session
from src.infrastructure.repositories import UserRepository
from src.application.services import UserService, AuthService

__all__ = [
    "get_user_service",
    "get_auth_service",
]


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(UserRepository(session=session))


def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(UserRepository(session=session))
