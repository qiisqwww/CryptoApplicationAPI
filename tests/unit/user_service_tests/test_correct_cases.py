import pytest

from src.application.services import UserService
from src.application.schemas import UserInputData, UserData
from src.application.utils import PasswdUtils


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "user_input_data, expected_user_data",
    [
        (
            UserInputData(
                username="user5",
                email="user5@gmail.com",
                password="user5"
            ),
            UserData(
                id=5,
                username="user5",
                email="user5@gmail.com",
                hashed_password=PasswdUtils.hashed_password("user5")
            )
        ),
        (
            UserInputData(
                username="user6",
                email="user6@gmail.com",
                password="user6"
            ),
            UserData(
                id=5,
                username="user6",
                email="user6@gmail.com",
                hashed_password=PasswdUtils.hashed_password("user6")
            )
        )
    ]
)
async def test_register(
        user_input_data: UserInputData,
        expected_user_data: UserData,
        user_service: UserService
) -> None:
    user_data = await user_service.register(user_input_data)
    assert (user_data.username == expected_user_data.username and user_data.email == expected_user_data.email)
