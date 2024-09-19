from sqlalchemy.sql import select, insert

from src.application.repositories import IUserRepository
from src.application.schemas import UserInputData, UserCreateData, UserData
from src.entities.models import User


__all__ = [
    "UserService"
]


class UserService:
    _user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

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
