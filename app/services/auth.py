# app/services/auth.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import cast

from app.schemas.auth import SignUpRequest, LoginRequest, SignUpResponse, Token
from app.db.models.user import User 
from app.core.security import verify_password, get_password_hash, create_access_token

def register_user(db: Session, payload: SignUpRequest) -> SignUpResponse:
    """
    회원가입 서비스: 중복 ID/이메일 체크, 해시 비밀번호 저장
    """
    # username 또는 email 중복 체크
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return SignUpResponse(
        userId=cast(int, user.id),   # type: ignore[arg-type]  ← cast로 int타입임을 명시
        username=str(user.username)
    )

def authenticate_user(db: Session, payload: LoginRequest) -> Token:
    """
    로그인 서비스: 아이디/비번 검증, JWT 발급
    """
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    # JWT 토큰 발급 (user.id, user.username 등 포함)
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return Token(access_token=access_token)
