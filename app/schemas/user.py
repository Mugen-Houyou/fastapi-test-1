# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 객체에서 바로 변환 가능
