from fastapi import APIRouter

__all__ = [
    "register_router",
]


register_router = APIRouter(
    prefix="/register",
)

