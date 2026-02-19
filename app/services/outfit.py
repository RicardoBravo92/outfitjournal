from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.clothing import Clothing
from ..schemas.outfit import OutfitCreate, OutfitUpdate
from sqlalchemy.exc import NoResultFound
from ..models.clothing import Clothing
from ..models.outfit import Outfit
from ..models.user import User


class OutfitService:

    def get_outfits(self, db: Session,skip:int,limit:int,current_user:User):
        outfits = db.query(Outfit).filter(
        Outfit.owner_id == current_user.id
             ).order_by(Outfit.used_date.desc()).offset(skip).limit(limit).all()
        return outfits

    def get_outfit(self, db: Session, outfit_id: int, current_user: User):
        outfit = db.query(Outfit).filter(Outfit.id == outfit_id, Outfit.owner_id == current_user.id).first()
        if not outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        return outfit

    def create_outfit(self, db: Session, outfit_in: OutfitCreate, current_user: User):
        outfit = Outfit(
            name=outfit_in.name,
            description=outfit_in.description,
            occasion=outfit_in.occasion,
            owner_id=current_user.id
        )
        db.add(outfit)
        db.commit()
        db.refresh(outfit)
        # Asociar prendas si clothes_ids está presente
        if hasattr(outfit_in, 'clothes_ids') and outfit_in.clothes_ids:
            clothes = db.query(Clothing).filter(Clothing.id.in_(outfit_in.clothes_ids), Clothing.owner_id == current_user.id).all()
            outfit.clothes = clothes
            db.commit()
            db.refresh(outfit)
        return outfit

    def update_outfit(self, db: Session, outfit_id: int, outfit_in: OutfitUpdate, current_user: User):
        outfit = db.query(Outfit).filter(Outfit.id == outfit_id, Outfit.owner_id == current_user.id).first()
        if not outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        for field, value in outfit_in.dict(exclude_unset=True).items():
            if field == "clothes_ids" and value is not None:
                clothes = db.query(Clothing).filter(Clothing.id.in_(value), Clothing.owner_id == current_user.id).all()
                outfit.clothes = clothes
            elif field != "clothes_ids":
                setattr(outfit, field, value)
        db.commit()
        db.refresh(outfit)
        return outfit

    def delete_outfit(self, db: Session, outfit_id: int, current_user: User):
        outfit = db.query(Outfit).filter(Outfit.id == outfit_id, Outfit.owner_id == current_user.id).first()
        if not outfit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outfit not found")
        db.delete(outfit)
        db.commit()
        return {"ok": True}


