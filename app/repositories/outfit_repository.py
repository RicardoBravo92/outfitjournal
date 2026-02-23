from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.outfit import Outfit
from app.schemas.outfit import OutfitCreate , OutfitUpdate
from sqlalchemy import select
from ..models.user import User

class OutfitRepository(BaseRepository[Outfit, OutfitCreate, OutfitUpdate]):
    
    async def get_user_outfits(self, db: AsyncSession, skip:int,limit:int,current_user:User):
        outfits = db.query(Outfit).filter(
        Outfit.owner_id == current_user.id
             ).order_by(Outfit.used_date.desc()).offset(skip).limit(limit).all()
        return outfits
    
    async def get_outfit_by_id(self, db: AsyncSession, outfit_id: int, current_user: User) -> Optional[Outfit]:
        query = select(Outfit).where(Outfit.id == outfit_id, Outfit.owner_id == current_user.id)
        result = await db.execute(query)
        outfit = result.scalar_one_or_none()
        return outfit
    
   
Outfit_repository = OutfitRepository(Outfit)