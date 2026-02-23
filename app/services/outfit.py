from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.clothing import Clothing
from ..schemas.outfit import OutfitCreate, OutfitUpdate
from sqlalchemy.exc import NoResultFound
from ..models.clothing import Clothing
from ..models.outfit import Outfit
from ..models.user import User
from ..repositories.outfit_repository import Outfit_repository


class OutfitService:
    
    def __init__(self, repository=Outfit_repository):
        self.repository = repository 

    def get_outfits(self, db: Session,skip:int,limit:int,current_user:User):
        return self.repository.get_user_outfits(db,skip,limit,current_user)

    async def get_outfit(self, db: Session, outfit_id: int, current_user: User):
        outfit = await self.repository.get_outfit_by_id(db, outfit_id, current_user)
        if not outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        return outfit

    async def create_outfit(self, db: Session, outfit_in: OutfitCreate, current_user: User):
        outfit = self.repository.create_outfit(db, outfit_in, current_user)
        if hasattr(outfit_in, 'clothes_ids') and outfit_in.clothes_ids:
            clothes = db.query(Clothing).filter(Clothing.id.in_(outfit_in.clothes_ids), Clothing.owner_id == current_user.id).all()
            outfit.clothes = clothes
            db.commit()
            db.refresh(outfit)
        return outfit

    async def update_outfit(self, db: Session, outfit_id: int, outfit_in: OutfitUpdate, current_user: User):
        Outfit = await self.repository.get_outfit_by_id(db, outfit_id, current_user)
        if not Outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        updated_outfit = self.repository.update_outfit(db, Outfit, outfit_in)
        return updated_outfit

    async def delete_outfit(self, db: Session, outfit_id: int, current_user: User):
        outfit = await self.repository.get_outfit_by_id(db, outfit_id, current_user)
        if not outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        self.repository.delete(db, outfit)
        return {"detail": "Outfit deleted successfully"}


