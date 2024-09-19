from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories import Repository
from src.application.repositories import IUserRepository
from src.entities.models import User

__all__ = [
    "UserRepository"
]


class UserRepository(Repository, IUserRepository):
    _model = type[User]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self._model = User

    async def insert_user(self) -> None:
        ...

    async def set_user_inactive(self, user_id: int) -> None:
        ...

    async def get_user_data(self, user_id: int) -> User:
        ...
