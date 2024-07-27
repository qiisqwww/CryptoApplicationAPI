from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update, insert, delete
from fastapi import Depends

from src.auth.models import User
from src.database import get_async_session

__all__ = [
    "UserService",
    "get_user_service"
]


class UserService:
    model: type[User]
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.model = User
        self.session = session

    async def check_user_exists(self, username: str, hashed_password: str) -> User:
        stmt = (select(self.model)
                .where(User.username == username)
                .where(User.hashed_password == hashed_password)
                )
        result = await self.session.execute(stmt)
        return result.scalars().first()


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)
