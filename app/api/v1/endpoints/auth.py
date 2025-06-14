# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.auth import SignUpRequest, SignUpResponse, LoginRequest, TokenPair, RefreshToken
from app.api.deps import get_db
from app.services.auth import register_user, authenticate_user, refresh_access_token

router = APIRouter()


@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    """회원 가입"""
    user = register_user(db, payload)
    return user

@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """JWT 로그인"""
    token = authenticate_user(db, payload)
    return token

@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshToken): # pair = {"refresh_token": "..."}
    """
    Refresh 토큰으로 새 access/refresh 쌍을 재발급
    참고! "쌍", 즉, 둘 다 재발급하는 것!
    """
    return refresh_access_token(payload.refresh_token)
