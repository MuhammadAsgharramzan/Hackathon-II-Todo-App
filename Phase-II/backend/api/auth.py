from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db.database import get_session
from models.user_model import UserCreate, UserResponse
from auth.auth_handlers import authenticate_user, create_user
from auth.auth_utils import create_access_token
from datetime import timedelta
from typing import Dict
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    try:
        db_user = create_user(session, user_create)

        # Return user info without sensitive data
        return UserResponse(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/login")
async def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token"""
    try:
        user = authenticate_user(session, login_request.email, login_request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create JWT token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.id},  # Use user ID as subject
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )