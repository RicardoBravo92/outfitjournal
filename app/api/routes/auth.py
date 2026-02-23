from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ...core.database import get_db
from ...core.security import create_access_token
from ...models.user import User as UserModel
from ...schemas.token import Token
from ...schemas.user import UserCreate, User as UserSchema, UserLogin
from ...core.config import settings
from ..dependencies.auth import get_current_user


from ...services.user import UserService

router = APIRouter(prefix="/auth", tags=["authentication"])
user_service = UserService()

@router.post("/register", response_model=UserSchema)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(
    email: str, password: str,
    db: Session = Depends(get_db),
):
    try:
        token = await user_service.authenticate(db, email, password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        token = await user_service.authenticate(db, form_data.username, form_data.password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user