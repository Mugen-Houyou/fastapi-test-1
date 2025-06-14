# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.auth import SignUpRequest, SignUpResponse, LoginRequest, Token
from app.api.deps import get_db
from app.services.auth import register_user, authenticate_user

router = APIRouter()

@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    """회원 가입"""
    user = register_user(db, payload)
    return user

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """JWT 로그인"""
    token = authenticate_user(db, payload)
    return token
