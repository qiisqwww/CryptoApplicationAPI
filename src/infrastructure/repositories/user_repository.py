from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, select

from src.infrastructure.repositories import Repository
from src.application.repositories import IUserRepository
from src.application.schemas import UserCreateData
from src.entities.models import User

__all__ = [
    "UserRepository"
]


class UserRepository(Repository, IUserRepository):
    _model = type[User]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._model = User

    async def insert_user(self, user_create_data: UserCreateData) -> User:
        stmt = insert(self._model).values(**user_create_data.dict()).returning(self._model)
        result = await self._session.execute(stmt)
        await self._session.commit()

        return result.scalars().first()

    # TODO this method
    async def set_user_inactive(self, user_id: int) -> None:
        ...

    async def find_user_by_id(self, user_id: int) -> User | None:
        stmt = (select(self._model).where(User.id == user_id))
        result = await self._session.execute(stmt)

        return result.scalar()

    async def find_user_by_username(self, username: str) -> User | None:
        stmt = (select(self._model).where(User.username == username))
        result = await self._session.execute(stmt)

        return result.scalar()

    async def find_user_by_email(self, email: str) -> User | None:
        stmt = (select(self._model).where(User.email == email))
        result = await self._session.execute(stmt)

        return result.scalar()
