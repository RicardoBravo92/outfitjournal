from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict
from datetime import datetime, timedelta
from ...core.database import get_db
from ...models.clothing import Clothing
from ...services.statistics import StatisticsService
from ...models.user import User
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/most-used")
def get_most_used_clothes(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StatisticsService.get_most_used_clothes(db, current_user, limit)

@router.get("/unused")
def get_unused_clothes(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StatisticsService.get_unused_clothes(db, current_user, days)

@router.get("/categories-summary")
def get_categories_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StatisticsService.get_categories_summary(db, current_user)

@router.get("/monthly-frequency")
def get_monthly_frequency(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return StatisticsService.get_monthly_frequency(db, current_user, months)