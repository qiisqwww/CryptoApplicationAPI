from fastapi import APIRouter

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

__all__ = [
    "auth_router"
]


auth_router = APIRouter(prefix="/user")
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["Authentication"],
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Registration"]
)
