# app/db/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base import Base  # declarative_base() 로 생성해둔 공통 Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # 이거는 DB상 index 개념!!  
    username = Column(String(32), unique=True, nullable=False, index=True) # 이게 한국어로 흔히 말하는 '아이디'.
    lastname = Column(String(128), unique=False, nullable=True, index=True) # 유저의 성씨
    firstname = Column(String(128), unique=False, nullable=False, index=True) # 유저의 이름
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Optional: 유저 정보 표시
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
