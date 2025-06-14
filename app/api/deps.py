# app/api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.core.config import settings
from app.crud.user import get_user_by_id
from app.schemas.user import UserOut

# 1. DB 세션 Dependency
def get_db() -> Generator:
    """
    요청 시마다 DB 세션을 생성하고,
    요청이 끝나면 세션을 종료합니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. JWT 인증된 현재 유저 반환 Dependency
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> UserOut:
    """
    JWT 토큰으로부터 현재 로그인된 유저 정보를 반환합니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception
        # 위 부분의 이전 코드:
        # user_id: int = payload.get("sub")
        # if user_id is None:
        #     raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user

# 3. (Optional) 관리자 권한 확인용 Dependency
def get_current_admin(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    """
    관리자만 접근 가능한 API 보호용 Dependency
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
