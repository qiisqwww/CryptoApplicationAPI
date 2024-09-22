from fastapi import APIRouter

from .login_router import login_router
from .refresh_token_router import refresh_token_router

__all__ = [
    "auth_router"
]


auth_router = APIRouter()
auth_router.include_router(login_router)
auth_router.include_router(refresh_token_router)
