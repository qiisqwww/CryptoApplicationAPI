from fastapi import APIRouter

from .login_router import login_router
from .register_router import register_router

__all__ = [
    "auth_router"
]

auth_router = APIRouter(prefix="/user")
auth_router.include_router(login_router)
auth_router.include_router(register_router)
