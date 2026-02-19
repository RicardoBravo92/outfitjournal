from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..services.user import get_user_by_email, get_user_by_username, create_user
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash, verify_password

class AuthService:
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        # Check if email exists
        if get_user_by_email(db, email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        
        # Check if username exists
        if get_user_by_username(db, username=user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )
            
        # Hash password and create user model
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )
        
        # Save to database via CRUD
        return create_user(db, db_user)

    def authenticate_user(self, db: Session, username: str, password: str):
        user = get_user_by_username(db, username=username)
        if not user:
            # Try email if username not found
            user =  get_user_by_email(db, email=username)
            
        if not user:
            return False
            
        if not verify_password(password, user.hashed_password):
            return False
            
        return user
