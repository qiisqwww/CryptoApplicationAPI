from src.application.repositories import IUserRepository
from src.application.schemas import UserCreateData
from src.entities import User

from tests.unit.mocks.users_list import users_list

__all__ = [
    "MockUserRepository",
]


class MockUserRepository(IUserRepository):
    users: list[User]

    def __init__(self) -> None:
        self.users = users_list.copy()

    async def insert_user(self, user_create_data: UserCreateData) -> User:
        created_user = User(
            id=self.users[-1].id + 1,
            username=user_create_data.username,
            email=user_create_data.email,
            hashed_password=user_create_data.hashed_password,
            is_active=user_create_data.is_active,
            is_superuser=user_create_data.is_superuser,
            is_verified=user_create_data.is_verified
        )

        self.users.append(created_user)
        return created_user

    async def set_user_inactive(self, user_id: int) -> None:
        for user in self.users:
            if user.id == user_id:
                user.is_active = False

    async def find_user_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user

        return None

    async def find_user_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user

        return None

    async def find_user_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user

        return None
