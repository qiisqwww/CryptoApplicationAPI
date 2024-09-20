from src.application.repositories import IUserRepository
from src.application.schemas import UserInputData, UserCreateData, UserData


__all__ = [
    "UserService"
]


class UserService:
    _user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    # TODO: добавить проверки (не зарегестрирован ли пользователь и т. д.)
    async def register_user(self, user_register_data: UserInputData, hashed_password: str) -> UserData:
        user_create_data = UserCreateData.get_from_register_data(user_register_data, hashed_password)

        user = await self._user_repository.register_user(user_create_data)
        return UserData.from_orm(user)

    async def get_user_by_username(self, username: str) -> UserData | None:
        user = await self._user_repository.get_user_by_username(username)
        return UserData.from_orm(user) if user else None

    async def get_user_by_id(self, user_id: str) -> UserData | None:
        user = await self._user_repository.get_user_by_id(user_id)
        return UserData.from_orm(user) if user else None

    async def get_user_by_email(self, email: str) -> UserData | None:
        user = await self._user_repository.get_user_by_email(email)
        return UserData.from_orm(user) if user else None
