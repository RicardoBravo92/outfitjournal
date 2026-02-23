from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.clothing_repository import Clothing_repository
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.clothing import Clothing
from ..models.user import User
from ..schemas.clothing import ClothingCreate , ClothingUpdate
from ..core.security import get_password_hash, verify_password
from .cloudinary_service import CloudinaryService


class ClothingService:
    def __init__(self):
        self.repository = Clothing_repository   

    async def create_clothing(self, db: Session, clothing_data: ClothingCreate, current_user: User, image=None) -> Clothing:
        """Create a new clothing item with optional image upload to Cloudinary"""
        image_url = None
        if image and image.filename:
            try:
                image_url = CloudinaryService.upload_image(image, folder=f"users/{current_user.id}")
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error uploading image"
                )      
        clothing_in_dict = clothing_data.dict()
        clothing_in_dict["image_url"] = image_url
        clothing_in_dict["owner_id"] = current_user.id
        clothing = await self.repository.create(db, ClothingCreate(**clothing_in_dict))
        return clothing
    
    async def get_user_clothes(self,db: Session, current_user:User,skip:int,limit:int,is_active:bool,category:str):
        return await self.repository.get_user_clothes(db, current_user, skip, limit, is_active, category)

    async def get_clothing_by_id(self,db: Session, clothing_id:int,current_user:User):
        clothing = await self.repository.get_clothing_by_id(db, clothing_id, current_user)
        if not clothing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothing not found"
            )
        return clothing
    
    async def update_clothing(self,db: Session, clothing_id:int,clothing_update:ClothingUpdate,current_user:User):
     
        db_clothing = await self.repository.get_clothing_by_id(db, clothing_id, current_user)        
        if not db_clothing:
            raise HTTPException(status_code=404, detail="Clothing item not found")        
        return await self.repository.update_clothing(db, db_clothing, clothing_update)
    
    async def delete_clothing(self,db: Session, clothing_id:int,current_user:User):
        db_clothing = await self.repository.get_clothing_by_id(db, clothing_id, current_user)
        if not db_clothing:
            raise HTTPException(status_code=404, detail="Clothing item not found")
        return await self.repository.delete_clothing(db, db_clothing)