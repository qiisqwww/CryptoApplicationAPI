from fastapi import APIRouter

from .auth import auth_router
from .user_management import user_management_router

__all__ = [
    "root_router",
]

root_router = APIRouter()
root_router.include_router(auth_router)
root_router.include_router(user_management_router)
