from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict
from datetime import datetime, timedelta
from ...core.database import get_db
from ...models.clothing import Clothing, Outfit
from ...models.user import User
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/most-used")
def get_most_used_clothes(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clothes = db.query(Clothing).filter(
        Clothing.owner_id == current_user.id,
        Clothing.is_active == True
    ).order_by(desc(Clothing.times_used)).limit(limit).all()
    
    return [
        {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "times_used": c.times_used,
            "last_used": c.last_used,
            "image_url": c.image_url
        }
        for c in clothes
    ]

@router.get("/unused")
def get_unused_clothes(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cutoff_date = datetime.now() - timedelta(days=days)
    
    clothes = db.query(Clothing).filter(
        Clothing.owner_id == current_user.id,
        Clothing.is_active == True,
        (Clothing.last_used < cutoff_date) | (Clothing.last_used.is_(None))
    ).all()
    
    return [
        {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "last_used": c.last_used,
            "image_url": c.image_url
        }
        for c in clothes
    ]

@router.get("/categories-summary")
def get_categories_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(
        Clothing.category,
        func.count(Clothing.id).label('total'),
        func.sum(func.cast(Clothing.is_active, func.Integer)).label('active')
    ).filter(Clothing.owner_id == current_user.id).group_by(Clothing.category).all()
    
    return [
        {
            "category": c[0],
            "total": c[1],
            "active": c[2] or 0
        }
        for c in categories
    ]

@router.get("/monthly-frequency")
def get_monthly_frequency(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cutoff_date = datetime.now() - timedelta(days=30 * months)
    
    outfits = db.query(
        func.date_trunc('month', Outfit.used_date).label('month'),
        func.count(Outfit.id).label('total')
    ).filter(
        Outfit.owner_id == current_user.id,
        Outfit.used_date >= cutoff_date
    ).group_by('month').order_by('month').all()
    
    return [
        {
            "month": o[0].strftime("%Y-%m"),
            "total": o[1]
        }
        for o in outfits
    ]