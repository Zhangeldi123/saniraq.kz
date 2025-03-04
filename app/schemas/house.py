from pydantic import BaseModel
from typing import Optional

class HouseBase(BaseModel):
    price: int
    address: str
    area: int
    rooms_count: int
    description: str

class HouseCreate(HouseBase):
    pass

class HouseUpdate(HouseBase):
    price: Optional[int] = None
    address: Optional[str] = None
    area: Optional[int] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None

class HouseResponse(HouseBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True