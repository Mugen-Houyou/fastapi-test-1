# app/crud/user.py

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.user import User


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    특정 user_id에 해당하는 유저를 반환합니다.
    없으면 None을 반환합니다.
    """
    return db.query(User).filter(User.id == user_id).first()
