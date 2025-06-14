# app/db/models/comment.py

"""
SQLAlchemy ORM 모델: Comment (댓글 & 대댓글)

- 게시글(Post)과 작성자(User) 모두에 FK
- parent_id 로 자기 참조하여 '대댓글' 트리 구현
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# 타입 검사 전용 import (순환 참조 방지)
if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.post import Post


class Comment(Base):
    __tablename__ = "comments"

    # ────────────────────────── 컬럼 ──────────────────────────
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 댓글 트리 관리 (NULL이면 최상위 댓글)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
    )
    depth: Mapped[int] = mapped_column(default=0, nullable=False)

    # FK: Post / User
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ────────────────────────── 관계 ──────────────────────────
    author: Mapped["User"] = relationship(
        "User",
        back_populates="comments",
        lazy="joined",
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
    )

    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="children",
    )

    children: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Comment.created_at.asc()",
    )

    # ────────────────────────── 메타 ──────────────────────────
    def __repr__(self) -> str:  # pragma: no cover
        return f"<Comment id={self.id} post_id={self.post_id} depth={self.depth}>"
