from abc import ABC, abstractmethod

from src.entities.models import User

__all__ = [
    "IUserRepository"
]


class IUserRepository(ABC):
    @abstractmethod
    async def insert_user(self) -> None:
        ...

    @abstractmethod
    async def set_user_inactive(self, user_id: int) -> None:
        ...

    @abstractmethod
    async def get_user_data(self, user_id: int) -> User:
        ...
