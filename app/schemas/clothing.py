from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ClothingBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    is_active: bool = True

class ClothingCreate(ClothingBase):
    pass

class ClothingUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Clothing(ClothingBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    times_used: int
    last_used: Optional[datetime] = None
    owner_id: int
    
    class Config:
        from_attributes = True