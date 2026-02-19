from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ...core.database import get_db
from ...models.clothing import Outfit, Clothing
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
    db_outfit = Outfit(
        name=outfit_data.name,
        description=outfit_data.description,
        occasion=outfit_data.occasion,
        owner_id=current_user.id
    )
    db.add(db_outfit)
    db.flush()
    
    for clothing_id in outfit_data.clothes_ids:
        clothing = db.query(Clothing).filter(
            Clothing.id == clothing_id,
            Clothing.owner_id == current_user.id
        ).first()
        
        if clothing:
            db_outfit.clothes.append(clothing)
            clothing.times_used += 1
            clothing.last_used = datetime.now()
    
    db.commit()
    db.refresh(db_outfit)
    return db_outfit

@router.put("/{outfit_id}", response_model=OutfitSchema)
def update_outfit(
    outfit_id: int,
    outfit_update: OutfitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_outfit = db.query(Outfit).filter(
        Outfit.id == outfit_id,
        Outfit.owner_id == current_user.id
    ).first()
    
    if not db_outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    
    for key, value in outfit_update.dict(exclude_unset=True).items():
        if key != "clothes_ids":
            setattr(db_outfit, key, value)
    
    if outfit_update.clothes_ids is not None:
        db_outfit.clothes = []
        for clothing_id in outfit_update.clothes_ids:
            clothing = db.query(Clothing).filter(
                Clothing.id == clothing_id,
                Clothing.owner_id == current_user.id
            ).first()
            if clothing:
                db_outfit.clothes.append(clothing)
    
    db.commit()
    db.refresh(db_outfit)
    return db_outfit

@router.delete("/{outfit_id}")
def delete_outfit(
    outfit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_outfit = db.query(Outfit).filter(
        Outfit.id == outfit_id,
        Outfit.owner_id == current_user.id
    ).first()
    
    if not db_outfit:
        raise HTTPException(status_code=404, detail="Outfit not found")
    
    db.delete(db_outfit)
    db.commit()
    
    return {"message": "Outfit deleted successfully"}