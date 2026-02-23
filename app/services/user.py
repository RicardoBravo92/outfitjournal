from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash, verify_password
from app.repositories.user_repository import user_repository

class UserService:
    
    def __init__(self):
        self.repository = user_repository

    async def create_user(self, db: Session, user_data: UserCreate) -> User:
        existing = await self.repository.get_by_email(db, user_data.email)
        if existing:
            raise ValueError("Email already registered")

        user_in_dict = user_data.dict()
        user_in_dict["hashed_password"] = get_password_hash(user_in_dict.pop("password"))

        user = await self.repository.create(db, UserCreate(**user_in_dict))
        return user
        
    async def authenticate(
        self,
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        user = await self.repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user