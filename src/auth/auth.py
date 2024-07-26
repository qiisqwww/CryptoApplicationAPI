from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users import FastAPIUsers

from src.config import SECRET, TOKEN_LIFETIME
from src.auth.models import User
from src.auth.manager import get_user_manager

__all__ = [
    "auth_backend",
    "fastapi_users"
]


bearer_transport = BearerTransport(tokenUrl="api/auth/token/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
