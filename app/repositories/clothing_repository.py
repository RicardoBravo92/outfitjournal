from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.clothing import Clothing
from app.schemas.clothing import ClothingCreate, ClothingUpdate
from sqlalchemy import select
from ..models.user import User

class ClothingRepository(BaseRepository[Clothing, ClothingCreate, ClothingUpdate]):
    
    async def get_user_clothes(self, db: AsyncSession, current_user:User,skip:int,limit:int,is_active:bool,category:str):
        """Get all clothes for the current user"""
        query = select(Clothing).where(Clothing.owner_id == current_user.id)
    
        if is_active is not None:
            query = query.where(Clothing.is_active == is_active)
    
        if category:
            query = query.where(Clothing.category == category)
    
        result = await db.execute(query.order_by(Clothing.created_at.desc()).offset(skip).limit(limit))
        clothes = result.scalars().all()
        return clothes
    
    async def get_clothing_by_id(self, db: AsyncSession, clothing_id: int, current_user: User) -> Optional[Clothing]:
        """Get a clothing item by ID"""
        query = select(Clothing).where(Clothing.id == clothing_id, Clothing.owner_id == current_user.id)
        result = await db.execute(query)
        clothing = result.scalar_one_or_none()
        return clothing
    
    
Clothing_repository = ClothingRepository(Clothing)