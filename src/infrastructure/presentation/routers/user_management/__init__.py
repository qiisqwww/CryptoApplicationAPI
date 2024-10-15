from fastapi import APIRouter

from .register_router import register_router
from .me_router import me_router
from .exists_router import exists_router

__all__ = [
    "user_management_router"
]


user_management_router = APIRouter(prefix="/user")
user_management_router.include_router(register_router)
user_management_router.include_router(me_router)
user_management_router.include_router(exists_router)
