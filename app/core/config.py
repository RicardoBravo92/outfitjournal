from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    # CORS: comma-separated origins, e.g. https://yourapp.onrender.com,https://www.yourapp.com
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")

    class Config:
        env_file = ".env"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

settings = Settings()