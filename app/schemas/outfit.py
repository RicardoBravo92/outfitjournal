from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .clothing import Clothing

class OutfitBase(BaseModel):
    name: str
    description: Optional[str] = None
    occasion: Optional[str] = None

class OutfitCreate(OutfitBase):
    clothes_ids: List[int]

class OutfitUpdate(OutfitBase):
    clothes_ids: Optional[List[int]] = None
    used_date: Optional[datetime] = None

class Outfit(OutfitBase):
    id: int
    created_at: datetime
    used_date: datetime
    owner_id: int
    clothes: List[Clothing] = []
    
    class Config:
        from_attributes = True