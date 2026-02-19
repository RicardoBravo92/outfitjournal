
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models.user import User
from ...schemas.clothing import ClothingSchema, ClothingCreate, ClothingUpdate
from ...services.Clothing import ClothingService
from ..dependencies.auth import get_current_user
import logging

router = APIRouter(prefix="/clothes", tags=["clothes"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ClothingSchema])
def get_clothes(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return  ClothingService.get_user_clothes(db,current_user,skip,limit,is_active,category)
    

@router.get("/{clothing_id}", response_model=ClothingSchema)
def get_clothing(
    clothing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ClothingService.get_clothing_by_id(
        db,clothing_id,current_user
    )

@router.post("/", response_model=ClothingSchema, status_code=status.HTTP_201_CREATED)
async def create_clothing(
    db: AsyncSession = Depends(get_db),
    clothing_data: ClothingCreate,
    current_user: User = Depends(get_current_user)
):
        try:
        clothing = await ClothingService.create_clothing(db, create_clothing,clothing_data,current_user)
        return clothing
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{clothing_id}", response_model=ClothingSchema)
def update_clothing(
    clothing_id: int,
    clothing_update: ClothingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   return ClothingService.update_clothing(
        db,clothing_id,clothing_update,current_user
        )   

@router.delete("/{clothing_id}")
async def delete_clothing(
    clothing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ClothingService.delete_clothing(db,clothing_id,current_user)
    