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
    from app.db.models.board import Board


class Post(Base):
    """
    게시글 테이블
    """
    __tablename__ = "posts"

    # 컬럼 
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    board_id: Mapped[int] = mapped_column( 
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 관계 
    board: Mapped["Board"] = relationship( # Board ➜ Post 방향의 관계 컬렉션 —— 1개의 보드가 n개의 포스트를 가짐
        "Board", 
        back_populates="posts"
    )

    author: Mapped["User"] = relationship( # Post ➜ User 방향의 관계 컬렉션 —— 1개의 게시글이 1개의 유저를 가짐
        "User",
        back_populates="posts",
        lazy="joined",
    )

    comments: Mapped[list["Comment"]] = relationship( # Post ➜ list["Comment"] 방향의 관계 컬렉션 —— 1개의 게시글이 n개의 댓글을 가짐
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    files: Mapped[list["File"]] = relationship( # Post ➜ list["File"] 방향의 관계 컬렉션 —— 1개의 게시글이 n개의 파일을 가짐
        "File", 
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # 메타데이터
    # Returns a string representation of the Post instance for debugging and logging purposes.
    # The returned string includes the class name and key identifying attributes (`id` and `title`), 
    # which helps developers quickly understand which specific Post object is being referenced.
    def __repr__(self) -> str:  # pragma: no cover
        """
        이 __repr__ 메서드는 Post 객체의 전체 데이터(본문, 작성자 등)가 아니라,
        객체를 구분할 수 있는 id와 title, board_id만을 보여줌.
        """
        return f"<Post id={self.id} title={self.title!r} board_id={self.board_id}>"
