from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.clothing import Clothing
from ..models.user import User
from ..schemas.clothing import ClothingCreate , ClothingUpdate
from ..core.security import get_password_hash, verify_password
from .cloudinary_service import CloudinaryService


class ClothingService:
    def create_clothing(self, db: Session, clothing_data: ClothingCreate, current_user: User, image=None) -> Clothing:
        """Create a new clothing item with optional image upload to Cloudinary"""
        image_url = None
        if image and image.filename:
            try:
                image_url = CloudinaryService.upload_image(image, folder=f"users/{current_user.id}")
            except Exception as e:
                # logger.error(f"Error uploading image: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error uploading image"
                )
        db_clothing = Clothing(
            name=clothing_data.name,
            category=clothing_data.category,
            description=clothing_data.description,
            is_active=clothing_data.is_active if hasattr(clothing_data, 'is_active') else True,
            image_url=image_url,
            owner_id=current_user.id
        )
        db.add(db_clothing)
        db.commit()
        db.refresh(db_clothing)
        return db_clothing
    
    def get_user_clothes(self,db: Session, current_user:User,skip:int,limit:int,is_active:bool,category:str):
        """Get all clothes for the current user"""
        query = db.query(Clothing).filter(Clothing.owner_id == current_user.id)
    
        if is_active is not None:
            query = query.filter(Clothing.is_active == is_active)
    
        if category:
            query = query.filter(Clothing.category == category)
    
        clothes = query.order_by(Clothing.created_at.desc()).offset(skip).limit(limit).all()
        return clothes

    def get_clothing_by_id(self,db: Session, clothing_id:int,current_user:User):
        """Get a clothing item by ID"""
        clothing = db.query(Clothing).filter(Clothing.id == clothing_id,Clothing.owner_id == current_user.id).first()
        if not clothing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothing not found"
            )
        return clothing
    
    def update_clothing(self,db: Session, clothing_id:int,clothing_update:ClothingUpdate,current_user:User):
        """Update a clothing item"""
        db_clothing = db.query(Clothing).filter(
            Clothing.id == clothing_id,
            Clothing.owner_id == current_user.id
        ).first()
        
        if not db_clothing:
            raise HTTPException(status_code=404, detail="Clothing item not found")
        
        for key, value in clothing_update.dict(exclude_unset=True).items():
            setattr(db_clothing, key, value)
        
        db.commit()
        db.refresh(db_clothing)
        return db_clothing
    
    def delete_clothing(self,db: Session, clothing_id:int,current_user:User):
        """Delete a clothing item"""
        db_clothing = db.query(Clothing).filter(
            Clothing.id == clothing_id,
            Clothing.owner_id == current_user.id
        ).first()
        
        if not db_clothing:
            raise HTTPException(status_code=404, detail="Clothing item not found")
        
        db.delete(db_clothing)
        db.commit()
        return {"message": "Clothing item deleted successfully"}