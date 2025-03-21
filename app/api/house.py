from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository.house import HousesRepository
from ..repository.comment import CommentsRepository
from ..schemas.house import HouseCreate, HouseUpdate
from fastapi import Request
from ..schemas.comment import CommentCreate, CommentUpdate
from jose import JWTError, jwt
import os
from jose import JWTError  # Import JWTError explicitly
from fastapi import Body
from ..schemas.house import PaginatedHouseResponse


house_router = APIRouter(prefix="/shanyraks", tags=["house"])

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


    
@house_router.get("", response_model=PaginatedHouseResponse)
def search_houses(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    type: Optional[str] = Query(None, pattern="^(sell|rent)$"),
    rooms_count: Optional[int] = Query(None, ge=1),
    price_from: Optional[int] = Query(None, ge=0),
    price_until: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    repo = HousesRepository(db)
    
    houses = repo.get_filtered_houses(
        limit=limit,
        offset=offset,
        type=type,
        rooms_count=rooms_count,
        price_from=price_from,
        price_until=price_until
    )
    
    total = repo.get_total_count(
        type=type,
        rooms_count=rooms_count,
        price_from=price_from,
        price_until=price_until
    )
    
    return PaginatedHouseResponse(
        total=total,
        objects=houses
    )

@house_router.post("")
def create_new_house(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),  # This might not be receiving the token
    price: int = Form(...),
    address: str = Form(...),
    area: int = Form(...),
    rooms_count: int = Form(...),
    description: str = Form(...)
):
    print(f"User ID in create_new_house: {user_id}")  # Debugging user_id
    house_data = HouseCreate(price=price, address=address, area=area, rooms_count=rooms_count, description=description)
    return HousesRepository(db).create_house(house_data, user_id)

@house_router.get("/{id}")
def read_house(id: int, db: Session = Depends(get_db)):
    return HousesRepository(db).get_house(id)

@house_router.patch("/{id}")
def update_existing_house(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
    price: int = Form(None),
    address: str = Form(None),
    area: int = Form(None),
    rooms_count: int = Form(None),
    description: str = Form(None)
):
    house = HousesRepository(db).get_house(id)
    if not house or house.owner_id != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own posts")
    house_data = HouseUpdate(price=price, address=address, area=area, rooms_count=rooms_count, description=description)
    return HousesRepository(db).update_house(id, house_data, user_id)

@house_router.delete("/{id}")
def delete_existing_house(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    house = HousesRepository(db).get_house(id)
    if not house or house.owner_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")
    return HousesRepository(db).delete_house(id, user_id)


@house_router.post("/{id}/comments")
def add_comment(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
    text: str = Form(...)
):
    comment_data = CommentCreate(text=text)  # ✅ Pydantic model
    return CommentsRepository(db).create_comment(id, user_id, comment_data.text)  # ✅ Pass only the text value


@house_router.patch("/{id}/comments/{comment_id}")
def edit_comment(
    id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
    text: str = Body(...)
):
    comment = CommentsRepository(db).get_comment(comment_id)
    if not comment or comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own comments")
    return CommentsRepository(db).update_comment(id, comment_id, user_id, text)



@house_router.delete("/{id}/comments/{comment_id}")
def remove_comment(id: int, comment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    comment = CommentsRepository(db).get_comment(comment_id)
    house = HousesRepository(db).get_house(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != user_id and house.owner_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments or if you are the post author")
    return CommentsRepository(db).delete_comment(id, comment_id, user_id)
