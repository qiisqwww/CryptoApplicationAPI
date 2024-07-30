from fastapi import APIRouter

#  src.auth.auth import auth_backend, fastapi_users
# from src.auth.schemas import UserRead, UserCreate
from src.routers import login_router, register_router

__all__ = [
    "auth_router"
]


auth_router = APIRouter(prefix="/user")
auth_router.include_router(login_router)
auth_router.include_router(register_router)
