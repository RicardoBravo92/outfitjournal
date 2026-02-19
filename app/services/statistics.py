from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from ..models.clothing import Clothing
from ..models.user import User

class StatisticsService:
    @staticmethod
    def get_most_used_clothes(db: Session, current_user: User, limit: int = 10):
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

    @staticmethod
    def get_unused_clothes(db: Session, current_user: User, days: int = 30):
        threshold_date = datetime.utcnow() - timedelta(days=days)
        clothes = db.query(Clothing).filter(
            Clothing.owner_id == current_user.id,
            Clothing.is_active == True,
            (Clothing.last_used == None) | (Clothing.last_used < threshold_date)
        ).all()
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

    @staticmethod
    def get_categories_summary(db: Session, current_user: User):
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

    @staticmethod
    def get_monthly_frequency(db: Session, current_user: User, months: int = 6):
        from ..models.clothing import Outfit
        cutoff_date = datetime.utcnow() - timedelta(days=30 * months)
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
