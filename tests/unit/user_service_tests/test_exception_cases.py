import pytest

from src.application.services import (
    UserService,
    UsernameAlreadyUsedException,
    EmailAlreadyUsedException,
)
from src.application.schemas import UserInputData


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "user_input_data",
    [
        UserInputData(
            username="user1",
            email="some_new_email@mail.ru",
            password="user's password"
        ),
        UserInputData(
            username="user3",
            email="another_new_email@mail.ru",
            password="any password"
        )
    ]
)
async def test_register_username_already_used(
        user_input_data: UserInputData,
        user_service: UserService,
) -> None:
    with pytest.raises(UsernameAlreadyUsedException):
        await user_service.register(user_input_data)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "user_input_data",
    [
        UserInputData(
            username="username not used yet",
            email="user1@gmail.com",
            password="user's password"
        ),
        UserInputData(
            username="random username",
            email="user3@gmail.com",
            password="any password"
        )
    ]
)
async def test_register_username_already_used(
        user_input_data: UserInputData,
        user_service: UserService,
) -> None:
    with pytest.raises(EmailAlreadyUsedException):
        await user_service.register(user_input_data)
