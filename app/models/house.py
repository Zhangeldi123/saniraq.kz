from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Houses(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, nullable=False, default=False)
    price = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    area = Column(Integer, nullable=False)
    rooms_count = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("new_users.id"), nullable=False)  # Changed from "users.id"
    owner = relationship("User", back_populates="houses")

    comments = relationship("Comments", back_populates="house", cascade="all, delete-orphan")
