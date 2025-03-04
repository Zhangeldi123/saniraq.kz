from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    phone: str
    password: str
    fullname: str
    city: str

class UserResponse(BaseModel):
    email: str
    phone: str
    fullname: str
    city: str

    class Config:
        from_attributes = True 