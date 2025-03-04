import bcrypt
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from typing import Optional

class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_userid(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = self.hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            fullname=user_data.fullname,  # Matches Pydantic schema
            city=user_data.city
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: int, user_data: UserCreate) -> Optional[User]:
        user = self.get_user_by_userid(user_id)
        if not user:
            return None
        
        if user_data.email:
            user.email = user_data.email
        if user_data.phone:
            user.phone = user_data.phone
        if user_data.fullname:
            user.fullname = user_data.fullname  # Matches Pydantic schema
        if user_data.city:
            user.city = user_data.city
        if user_data.password:
            user.password = self.hash_password(user_data.password)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user and self.verify_password(password, user.password):
            return user
        return None

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
