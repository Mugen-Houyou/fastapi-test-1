# app/core/security.py

from datetime import datetime, timedelta
from typing import Any, Dict, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# ------------------------------------------------------------------
# Password hashing / verification
# ------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    사용자가 입력한 평문 비밀번호(plain_password)가
    DB에 저장된 bcrypt 해시(hashed_password)와 일치하는지 확인합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    평문 비밀번호를 bcrypt 알고리즘으로 해싱하여 반환합니다.
    """
    return pwd_context.hash(password)


# ------------------------------------------------------------------
# JWT access-token 생성
# ------------------------------------------------------------------
ALGORITHM: str = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = getattr(
    settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60
)  # 설정 파일에 없으면 기본 60분


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Union[timedelta, None] = None,
) -> str:
    """
    주어진 payload(data)로 JWT access token을 생성합니다.

    Parameters
    ----------
    data : dict
        토큰에 포함될 사용자 정보(예: {"sub": user_id})
    expires_delta : timedelta | None
        만료 시간 델타(미지정 시 기본값 ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns
    -------
    str
        인코딩된 JWT 문자열
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
