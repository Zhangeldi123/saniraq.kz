from typing import List, Optional
from sqlalchemy.orm import Session
from models.house import Houses
from schemas.house import HouseCreate, HouseUpdate
from fastapi import HTTPException, status
from sqlalchemy import func
from schemas.house import HouseResponse

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

    def get_filtered_houses(
        self,
        limit: int,
        offset: int,
        type: Optional[str],
        rooms_count: Optional[int],
        price_from: Optional[int],
        price_until: Optional[int]
    ) -> List[HouseResponse]:
        query = self.db.query(Houses)
        
        # Применяем фильтры
        if type:
            query = query.filter(Houses.type == type)
        if rooms_count is not None:
            query = query.filter(Houses.rooms_count == rooms_count)
        if price_from is not None:
            query = query.filter(Houses.price >= price_from)
        if price_until is not None:
            query = query.filter(Houses.price <= price_until)
            
        # Сортировка и пагинация
        query = query.order_by(Houses.created_at.desc())
        return query.offset(offset).limit(limit).all()

    def get_total_count(
        self,
        type: Optional[str],
        rooms_count: Optional[int],
        price_from: Optional[int],
        price_until: Optional[int]
    ) -> int:
        query = self.db.query(func.count(Houses.id))
        
        if type:
            query = query.filter(Houses.type == type)
        if rooms_count is not None:
            query = query.filter(Houses.rooms_count == rooms_count)
        if price_from is not None:
            query = query.filter(Houses.price >= price_from)
        if price_until is not None:
            query = query.filter(Houses.price <= price_until)
            
        return query.scalar()