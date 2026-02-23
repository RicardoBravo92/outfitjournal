from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from ..models.clothing import Clothing
from ..models.outfit import Outfit
from ..models.user import User
from ..repositories.statistic_repository import StatisticRepository

class StatisticsService:

    def __init__(self, repository: StatisticRepository):
        self.repository = repository

    @staticmethod
    async def get_most_used_clothes(db: Session, current_user: User, limit: int = 10):
        return await StatisticRepository.get_most_used_clothes(db, current_user, limit)

    @staticmethod
    async def get_unused_clothes(db: Session, current_user: User, days: int = 30):
        return await StatisticRepository.get_unused_clothes(db, current_user, days)

    @staticmethod
    async def get_categories_summary(db: Session, current_user: User):
        return await StatisticRepository.get_categories_summary(db, current_user)

    @staticmethod
    async def get_monthly_frequency(db: Session, current_user: User, months: int = 6):
        return await StatisticRepository.get_monthly_frequency(db, current_user, months)
