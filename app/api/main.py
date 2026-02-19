from fastapi import APIRouter
from .routes import clothing, auth, outfit, statistics

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(outfit.router)
api_router.include_router(clothing.router)
api_router.include_router(statistics.router)


