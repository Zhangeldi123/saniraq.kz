from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from repository.user import UsersRepository
from schemas.user import UserResponse, UserCreate
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user/login")


user_router = APIRouter(prefix="/auth/user", tags=["user"])


SECRET_KEY = os.getenv("AUTH_SECRET", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def generate_access_token(user_id: int):
    expiration = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"user_id": user_id, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

def generate_refresh_token(user_id: int):
    expiration = datetime.now(tz=timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"user_id": user_id, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_refresh_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@user_router.post("", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    print(user_data.dict())
    users_repo = UsersRepository(db)
    existing_user = users_repo.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = users_repo.create_user(user_data)
    return UserResponse(id=user.id, email=user.email, fullname=user.fullname)



@user_router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    users_repo = UsersRepository(db)
    user = users_repo.authenticate_user(email, password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True, 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    
    return response



@user_router.patch("/me", response_model=UserResponse)
def update_user_profile(
    request: Request, user_data: UserCreate, db: Session = Depends(get_db)
):
    users_repo = UsersRepository(db)

    # Extract token from cookies
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    # Remove 'Bearer ' prefix before verifying the token
    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    user_id = verify_token(access_token)

    user = users_repo.get_user_by_userid(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = users_repo.update_user(user_id, user_data)
    return updated_user



@user_router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    users_repo = UsersRepository(db)

    # Extract token from cookies instead of using oauth2_scheme
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    # Remove 'Bearer ' prefix before verifying the token
    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    user_id = verify_token(access_token)
    
    user = users_repo.get_user_by_userid(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user



@user_router.post("/refresh")
def refresh_access_token(refresh_token: str = Form(...)):
    user_id = verify_refresh_token(refresh_token)
    new_access_token = generate_access_token(user_id)

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {new_access_token}", 
        httponly=True, 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response
