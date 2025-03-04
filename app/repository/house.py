from sqlalchemy.orm import Session
from models.house import Houses
from schemas.house import HouseCreate, HouseUpdate
from fastapi import HTTPException, status

class HousesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_houses(self):
        return self.db.query(Houses).all()

    def create_house(self, house_data: HouseCreate, user_id: int):
        house = Houses(**house_data.dict(), owner_id=user_id)
        self.db.add(house)
        self.db.commit()
        self.db.refresh(house)
        return house

    def get_house(self, house_id: int):
        house = self.db.query(Houses).filter(Houses.id == house_id).first()
        if not house:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
        return house

    def update_house(self, house_id: int, house_data: HouseUpdate, user_id: int):
        house = self.db.query(Houses).filter(Houses.id == house_id).first()
        if not house:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
        if house.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this house")
        
        for key, value in house_data.dict(exclude_unset=True).items():
            setattr(house, key, value)
        
        self.db.commit()
        self.db.refresh(house)
        return house

    def delete_house(self, house_id: int, user_id: int):
        house = self.db.query(Houses).filter(Houses.id == house_id).first()
        if not house:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")
        if house.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this house")
        
        self.db.delete(house)
        self.db.commit()
        return {"detail": "House deleted successfully"}
