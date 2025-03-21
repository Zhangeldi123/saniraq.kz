from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
from ..repository.favorites import FavoritesRepository
from ..schemas.user import UserResponse
import os
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user/login")
favorites_router = APIRouter(prefix="/auth/users/favorites/shanyraks", tags=["favorites"])
SECRET_KEY = os.getenv("AUTH_SECRET", "secret")

def get_current_user(request: Request):
    token = request.cookies.get("access_token")  # Retrieve token from cookies
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = token.replace("Bearer ", "")  # Remove prefix if present

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@favorites_router.post("/{id}")
def add_favorite_house(id: int, db: Session = Depends(get_db), user_id: UserResponse = Depends(get_current_user)):
    return FavoritesRepository(db).add_favorite(user_id, id)

@favorites_router.get("")
def show_favorites(db: Session = Depends(get_db), user_id: UserResponse = Depends(get_current_user)):
    return FavoritesRepository(db).get_favorites(user_id)

@favorites_router.delete("/{id}")
def delete_favorite_house(id: int, db: Session = Depends(get_db), user_id: UserResponse = Depends(get_current_user)):
    return FavoritesRepository(db).delete_favorite(user_id, id)
