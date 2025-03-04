from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "new_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    city = Column(String, nullable=False)


    houses = relationship("Houses", back_populates="owner", cascade="all, delete-orphan")
    
    comments = relationship("Comments", back_populates="user", cascade="all, delete-orphan")

    
