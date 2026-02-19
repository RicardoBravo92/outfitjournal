from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ...core.database import get_db
from ...models.clothing import Clothing
from ...models.outfit import Outfit
from ...models.user import User
from ...schemas.outfit import Outfit as OutfitSchema, OutfitCreate, OutfitUpdate
from ..dependencies.auth import get_current_user
from ...services.outfit import OutfitService

router = APIRouter(prefix="/outfits", tags=["outfits"])

@router.get("/", response_model=List[OutfitSchema])
def get_outfits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OutfitService.get_outfits(db,skip,limit,current_user)

@router.get("/{outfit_id}", response_model=OutfitSchema)
def get_outfit(
    outfit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OutfitService.get_outfit(db,outfit_id,current_user)

@router.post("/", response_model=OutfitSchema)
def create_outfit(
    outfit_data: OutfitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OutfitService.create_outfit(db,outfit_data,current_user)

@router.put("/{outfit_id}", response_model=OutfitSchema)
def update_outfit(
    outfit_id: int,
    outfit_update: OutfitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return OutfitService.update_outfit(db,outfit_id,outfit_update,current_user)

@router.delete("/{outfit_id}")
def delete_outfit(
    outfit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
   return OutfitService.delete_outfit(db,outfit_id,current_user)