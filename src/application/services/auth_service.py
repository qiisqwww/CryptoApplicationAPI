from src.application.repositories import IUserRepository
from src.application.schemas import Token, UserData
from src.application.token_type import TokenType
from src.application.auth_utils import AuthUtils


__all__ = [
    "UserWasNotFoundException",
    "UserIsNotActiveException",
    "UnexpectedTokenTypeException",
    "AuthService"
]


class UserWasNotFoundException(Exception):
    """
    Raised when a user wasn't found
    """


class UserIsNotActiveException(Exception):
    """
    Raised when a user isn't active
    """


class UnexpectedTokenTypeException(Exception):
    """
    Raised when an unexpected token type is given
    """


class AuthService:
    _user_repository: IUserRepository

    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def authenticate(self, username: str, password: str) -> Token:
        user = await self._user_repository.find_user_by_username(username)
        if not user or AuthUtils.password_valid(password, user.hashed_password):
            raise UserWasNotFoundException

        if not user.is_active:
            raise UserIsNotActiveException

        return Token(
            access_token=AuthUtils.create_token(user, TokenType.ACCESS),
            refresh_token=AuthUtils.create_token(user, TokenType.REFRESH)
        )

    async def authorize(self, token_credentials: dict) -> UserData:
        user = self._decode_token_by_type(token_credentials, TokenType.ACCESS)
        return user

    async def refresh_access_token(self, token_credentials: dict) -> Token:
        user = self._decode_token_by_type(token_credentials, TokenType.REFRESH)
        return Token(refresh_token=AuthUtils.create_token(user, TokenType.REFRESH))

    async def _decode_token_by_type(self, token_credentials: dict, expected_token_type: TokenType) -> UserData:
        payload = AuthUtils.decode_token(token_credentials)

        token_type = payload.get(TokenType.FIELD)
        if token_type != expected_token_type:
            raise UnexpectedTokenTypeException

        username = payload.get("sub")
        if not username:
            raise UserWasNotFoundException

        user = await self._user_repository.find_user_by_username(username)
        if not user:
            raise UserWasNotFoundException

        return user
