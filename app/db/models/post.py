# app/db/models/post.py

"""
SQLAlchemy ORM 모델: Post (게시글)

- SQLAlchemy 2.0 "Typed ORM" 스타일(Mapped, mapped_column)
- author(User) · comments(Comment) · files(File) 와 관계 설정
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base  # declarative_base() 로 생성해둔 공통 Base

# 타입 체커 전용 import (순환 참조 방지)
if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.comment import Comment
    from app.db.models.file import File


class Post(Base):
    """
    게시글 테이블
    """
    __tablename__ = "posts"

    # ────────────────────────── 컬럼 ──────────────────────────
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ────────────────────────── 관계 ──────────────────────────
    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
        lazy="joined",
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # ────────────────────────── 메타 ──────────────────────────
    def __repr__(self) -> str:  # pragma: no cover
        return f"<Post id={self.id!r} title={self.title!r}>"
