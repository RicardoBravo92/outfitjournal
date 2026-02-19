from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.clothing import Clothing
from ..models.user import User
from ..schemas.clothing import ClothingCreate,
from ..core.security import get_password_hash, verify_password
from ...services.cloudinary_service import CloudinaryService


class OutfitService:

    def get_outfits(self, db: Session,skip:int,limit:int,current_user:User):
        outfits = db.query(Outfit).filter(
        Outfit.owner_id == current_user.id
             ).order_by(Outfit.used_date.desc()).offset(skip).limit(limit).all()
        return outfits


