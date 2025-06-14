# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends

from app.schemas.user import UserOut
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    """내 정보 조회"""
    return current_user
