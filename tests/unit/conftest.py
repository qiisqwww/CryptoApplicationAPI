import pytest

import tests.unit.mocks.environment  # NEED TO BE IMPORTED BEFORE CODE TO SET ENVIRONMENT VALUES
from tests.unit.mocks.mock_user_repository import MockUserRepository

from src.application.services import AuthService, UserService


@pytest.fixture()
def auth_service() -> AuthService:
    return AuthService(
        MockUserRepository()
    )


@pytest.fixture()
def user_service() -> UserService:
    return UserService(
        MockUserRepository()
    )
