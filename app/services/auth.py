# app/services/auth.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import cast

from app.schemas.auth import SignUpRequest, LoginRequest, SignUpResponse, TokenPair
from app.db.models.user import User 
from app.core.security import verify_password, get_password_hash, create_access_token, verify_refresh_token, create_refresh_token
from jose import jwt

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
        lastname=payload.lastname,
        firstname=payload.firstname,
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

def authenticate_user(db: Session, payload: LoginRequest) -> TokenPair:
    """
    로그인 시, access + refresh 쌍으로 발급
    """
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )

    new_claims = {"sub": str(user.id), "username": user.username}

    return TokenPair(
        access_token=create_access_token(new_claims),
        refresh_token=create_refresh_token(new_claims),
    )


def refresh_access_token(refresh_token: str) -> TokenPair:
    """
    클라이언트가 제출한 refresh_token을 검증 후, 새 access+refresh 쌍 재발급
    참고! "쌍", 즉, 둘 다 재발급하는 것!
    """
    try:
        payload = verify_refresh_token(refresh_token)
    except:
    # except jwt.JWTError: # TODO: 이거 왜 없다고 뜨는지 모르겠지만 넘어가자.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_claims = {"sub": payload["sub"], "username": payload.get("username")}

    return TokenPair(
        access_token=create_access_token(new_claims),
        refresh_token=create_refresh_token(new_claims),
    )