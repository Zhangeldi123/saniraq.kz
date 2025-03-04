from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)


    user_id = Column(Integer, ForeignKey("new_users.id", ondelete="CASCADE"), nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id", ondelete="CASCADE"), nullable=False)



    user = relationship("User", back_populates="comments")
    house = relationship("Houses", back_populates="comments")