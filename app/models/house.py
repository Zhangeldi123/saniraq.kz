from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Houses(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    area = Column(Integer, nullable=False)
    rooms_count = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("new_users.id"), nullable=False)  # Changed from "users.id"
    owner = relationship("User", back_populates="houses")

    comments = relationship("Comments", back_populates="house", cascade="all, delete-orphan")
    favorites = relationship("Favorites", back_populates="house", cascade="all, delete")
