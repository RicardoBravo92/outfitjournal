from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User-specific repository."""
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def is_active(self, db: AsyncSession, user_id: int) -> bool:
        """Check if user is active."""
        user = await self.get(db, user_id)
        return user.is_active if user else False

user_repository = UserRepository(User)