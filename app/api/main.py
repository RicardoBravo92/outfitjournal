from fastapi import APIRouter

from app.api.routes import clothing, auth, outfit, statistics
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(outfit.router)
api_router.include_router(clothing.router)
api_router.include_router(statistics.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)