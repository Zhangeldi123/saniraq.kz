from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Optional

class HouseBase(BaseModel):
    price: int
    address: str
    area: int
    rooms_count: int
    description: str

class HouseCreate(BaseModel):
    type: str = Field(..., example="sell")
    
    @field_validator('type')
    def validate_type(cls, v):
        if v not in {"sell", "rent"}:
            raise ValidationError(
                "Type must be either 'sell' or 'rent'"
            )
        return v

class HouseUpdate(HouseBase):
    price: Optional[int] = None
    address: Optional[str] = None
    area: Optional[int] = None
    rooms_count: Optional[int] = None
    description: Optional[str] = None

from pydantic import BaseModel

class HouseResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: int
    rooms_count: int

    class Config:
        orm_mode = True

class PaginatedHouseResponse(BaseModel):
    total: int
    objects: List[HouseResponse]