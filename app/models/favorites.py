from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Favorites(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("new_users.id"), nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)

    house = relationship("Houses", back_populates="favorites")