from abc import ABC, abstractmethod

from src.application.schemas import UserCreateData
from src.entities.models import User

__all__ = [
    "IUserRepository"
]


class IUserRepository(ABC):
    @abstractmethod
    async def register_user(self, user_create_data: UserCreateData) -> User:
        ...

    @abstractmethod
    async def set_user_inactive(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...
