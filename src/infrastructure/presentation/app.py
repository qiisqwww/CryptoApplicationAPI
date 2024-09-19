from fastapi import FastAPI

from src.config import DEBUG, PROJECT_NAME, DOCS_URL, OPENAPI_URL
from src.infrastructure.presentation import exceptions_middleware
from src.infrastructure.presentation.routers import auth_router

__all__ = [
    "app_object"
]


openapi_url = OPENAPI_URL if DEBUG else None

app_object = FastAPI(
    title=PROJECT_NAME,
    debug=DEBUG,
    docs_url=DOCS_URL,
    openapi_url=openapi_url
)

app_object.middleware("http")(exceptions_middleware)
app_object.include_router(auth_router)
