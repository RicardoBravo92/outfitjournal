from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

outfit_clothing = Table(
    'outfit_clothing',
    Base.metadata,
    Column('outfit_id', Integer, ForeignKey('outfits.id', ondelete="CASCADE")),
    Column('clothing_id', Integer, ForeignKey('clothes.id', ondelete="CASCADE"))
)

class Outfit(Base):
    __tablename__ = "outfits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    occasion = Column(String(100), nullable=True)  # work, party, sport, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    used_date = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    owner = relationship("User", back_populates="outfits")
    clothes = relationship("Clothing", secondary=outfit_clothing, back_populates="outfits")
