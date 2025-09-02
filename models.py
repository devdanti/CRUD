from sqlalchemy import Column, Integer, String
from database import Base

class Foto(Base):
    __tablename__ = "foto"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_hash = Column(String(255), unique=True, nullable=False, index=True)
