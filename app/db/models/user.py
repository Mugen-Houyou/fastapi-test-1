# app/db/models/user.py

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base  # declarative_base() 로 생성해둔 공통 Base

# 타입 체커 전용 import (순환 참조 방지)
if TYPE_CHECKING:
    from app.db.models.post import Post
    from app.db.models.comment import Comment
    from app.db.models.file import File

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # 이거는 DB상 index 개념!!  
    username = Column(String(32), unique=True, nullable=False, index=True) # 이게 한국어로 흔히 말하는 '아이디'.
    lastname = Column(String(128), unique=False, nullable=True, index=True) # 유저의 성씨
    firstname = Column(String(128), unique=False, nullable=False, index=True) # 유저의 이름 - 얘는 필수
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # User가 쓴 모든 posts
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",  # 다수의 게시글 조회시 N+1 쿼리 방지용 
    )

    # User가 쓴 모든 comments(대댓글 포함)
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

    # User가 올린 모든 files
    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="uploader",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )


    # Optional: 유저 정보 표시
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
