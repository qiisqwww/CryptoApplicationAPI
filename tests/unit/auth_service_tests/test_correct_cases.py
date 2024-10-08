import pytest

from tests.unit.mocks.users_list import users_list

from src.application.services import AuthService
from src.application.utils import TokenUtils
from src.application.token_type import TokenType
from src.application.schemas import Token
from src.entities import User


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "username, password",
    [
        ("user1", "user1"),
        ("user3", "user3"),
    ]
)
async def test_authenticate(
        username: str,
        password: str,
        auth_service: AuthService
) -> None:
    token = await auth_service.authenticate(username, password)
    assert isinstance(token, Token) and token.access_token and token.refresh_token


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "access_token, expected",
    [
        (TokenUtils.create_token(users_list[0], TokenType.ACCESS), users_list[0]),
        (TokenUtils.create_token(users_list[2], TokenType.ACCESS), users_list[2])
    ]
)
async def test_authorize(access_token: str, expected: User, auth_service: AuthService) -> None:
    user = await auth_service.authorize(access_token)
    assert user == expected


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "refresh_token",
    [
        TokenUtils.create_token(users_list[0], TokenType.REFRESH),
        TokenUtils.create_token(users_list[2], TokenType.REFRESH)
    ]
)
async def test_refresh_access_token(refresh_token: str, auth_service: AuthService) -> None:
    token = await auth_service.refresh_access_token(refresh_token)
    assert isinstance(token, Token) and token.access_token and not token.refresh_token


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "token, expected_token_type, expected",
    [
        (TokenUtils.create_token(users_list[1], TokenType.ACCESS), TokenType.ACCESS, users_list[1]),
        (TokenUtils.create_token(users_list[2], TokenType.REFRESH), TokenType.REFRESH, users_list[2])
    ]
)
async def test_decode_token_by_type(
        token: str,
        expected_token_type: TokenType,
        expected: User,
        auth_service: AuthService
) -> None:
    user = await auth_service._decode_token_by_type(token, expected_token_type)
    assert user == expected
