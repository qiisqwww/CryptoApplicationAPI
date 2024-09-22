from fastapi import APIRouter

from .auth import auth_router
from .get_me import get_me_router
from .register_router import register_router

__all__ = [
    "user_router",
]

user_router = APIRouter(prefix="/user")
user_router.include_router(register_router)
user_router.include_router(auth_router)
user_router.include_router(get_me_router)
