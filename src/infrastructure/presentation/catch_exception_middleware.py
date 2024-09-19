from fastapi import Request
from fastapi.responses import JSONResponse

__all__ = [
    "exceptions_middleware",
]


async def exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(e)
        return JSONResponse({"detail": "Internal server error"},
                            status_code=500)
