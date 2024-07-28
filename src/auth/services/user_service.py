from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, insert
from fastapi import Depends

from src.auth.models import User
from src.auth.schemas import UserInputData, UserCreateData, UserData
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

    async def register_user(self, user_register_data: UserInputData, hashed_password: str) -> UserData:
        user_create_data = UserCreateData.get_from_register_data(user_register_data, hashed_password)

        stmt = insert(self.model).values(**user_create_data.dict()).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()

        return UserData.from_orm(result.scalars().first())

    async def get_user_by_username(self, username: str) -> UserData | None:
        stmt = (select(self.model).where(User.username == username))
        result = await self.session.execute(stmt)

        user = result.scalar()
        return UserData.from_orm(user) if user else None

    async def get_user_by_email(self, email: str) -> UserData | None:
        stmt = (select(self.model).where(User.email == email))
        result = await self.session.execute(stmt)

        user = result.scalar()
        return UserData.from_orm(user) if user else None


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)
