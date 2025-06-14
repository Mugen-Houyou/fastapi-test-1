# app/core/security.py

from datetime import datetime, timedelta
from typing import Any, Dict, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

ACCESS_SECRET_KEY: str = getattr(
    settings, "JWT_ACCESS_SECRET_KEY", settings.JWT_ACCESS_SECRET_KEY  # 없으면 access와 동일 시크릿
)

REFRESH_SECRET_KEY: str = getattr(
    settings, "JWT_REFRESH_SECRET_KEY", settings.JWT_REFRESH_SECRET_KEY 
)

ACCESS_TOKEN_EXPIRE_MINUTES: int = getattr(
    settings, "ACCESS_TOKEN_EXPIRE_MINUTES", settings.JWT_AC_MINS
)

REFRESH_TOKEN_EXPIRE_DAYS: int = getattr(
    settings, "REFRESH_TOKEN_EXPIRE_DAYS", settings.JWT_RF_DAYS
)

ALGORITHM: str = settings.ALGORITHM

# Password hashing / verification ~~
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    사용자가 입력한 평문 비밀번호(plain_password)가
    DB에 저장된 bcrypt 해시(hashed_password)와 일치하는지 확인
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    평문 비밀번호를 bcrypt 알고리즘으로 해싱하여 반환
    """
    return pwd_context.hash(password)
# ~~ Password hashing / verification


# JWT token 관련 ~~
def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    return _create_jwt(
        data,
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        ACCESS_SECRET_KEY,
    )

def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    길게 유지되는 Refresh 토큰 생성
    """
    return _create_jwt(
        data,
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        REFRESH_SECRET_KEY,
    )

def verify_refresh_token(token: str) -> dict[str, Any]:
    """
    Refresh 토큰 검증 & 페이로드 반환. 만료·위조 시 JWTError 발생
    """
    return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
# ~~ JWT token 관련


# 내부 헬퍼 ~~

def _create_jwt(data: Dict[str, Any], delta: timedelta, secret: str) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + delta})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

# ~~ 내부 헬퍼