import pytest

from tests.unit.mocks.users_list import users_list

from src.application.services import (
    AuthService,
    UserWasNotFoundException,
    UserIsNotActiveException, UnexpectedTokenTypeException
)
from src.application.utils import TokenUtils
from src.application.token_type import TokenType


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "username, password",
    [
        ("unregistered_user", "does_not_matter"),
        ("user3", "abra_kadabra")
    ]
)
async def test_authenticate_user_was_not_found(
        username: str,
        password: str,
        auth_service: AuthService
) -> None:
    with pytest.raises(UserWasNotFoundException):
        await auth_service.authenticate(username, password)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "username, password",
    [("user4", "user4")]
)
async def test_authenticate_user_is_not_active(
        username: str,
        password: str,
        auth_service: AuthService
) -> None:
    with pytest.raises(UserIsNotActiveException):
        await auth_service.authenticate(username, password)


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "token, expected_token_type",
    [
        (TokenUtils.create_token(users_list[0], TokenType.ACCESS), TokenType.REFRESH),
        (TokenUtils.create_token(users_list[0], TokenType.REFRESH), TokenType.ACCESS)
    ]
)
async def test_decode_token_by_type_unexpected_token_type(
        token: str,
        expected_token_type: TokenType,
        auth_service: AuthService
) -> None:
    with pytest.raises(UserWasNotFoundException):
        await auth_service.authenticate(token, expected_token_type)
