# app/api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.core.config import settings
from app.crud.user import get_user_by_id
from app.schemas.user import UserOut

# DB 세션 Dependency
def get_db() -> Generator:
    """
    요청 들어올 때마다 DB 세션을 생성하고,
    요청이 끝나면 세션을 종료
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT 인증된 현재 유저 반환 Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db = Depends(get_db)
) -> UserOut:
    """
    HTTP Bearer 토큰으로부터 현재 로그인된 유저 정보를 반환
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_oauth2(
    # token: str = Depends(oauth2_scheme),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db = Depends(get_db)
) -> UserOut:
    """
    중요! 이건 OAuth2 방식. HTTPBearer 말고 OAuth2PasswordBearer 쓰려면 이걸로 할 것.
    JWT 토큰으로부터 현재 로그인된 유저 정보를 반환
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET_KEY,
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

# 관리자 권한 확인용 Dependency - Optional
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
