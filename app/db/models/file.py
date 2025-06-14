# app/db/models/file.py

"""
SQLAlchemy ORM 모델: File (첨부파일 메타데이터)

- 실제 바이너리는 디스크나 S3 등 스토리지에 저장하고,
  DB에는 경로·키 등 메타만 기록
- 게시글(Post) 1:N 관계
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# 타입 체커 전용 import (순환 참조 방지)
if TYPE_CHECKING:
    from app.db.models.post import Post
    from app.db.models.user import User


class File(Base):
    """
    첨부파일 테이블
    """
    __tablename__ = "files"

    # 컬럼 
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 원본 파일명
    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    # 스토리지 상의 객체 키(또는 로컬 경로)
    object_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)

    # MIME type (예: image/png)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # 바이트 단위 크기
    size: Mapped[int] = mapped_column(Integer, nullable=False)

    # FK: Post / User
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    uploader_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    # 관계 
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="files",
    )
    uploader: Mapped["User"] = relationship(
        "User",
        back_populates="files",
        lazy="joined",
    )

    # 메타데이터
    def __repr__(self) -> str:  # pragma: no cover
        return f"<File id={self.id} filename={self.filename!r}>"
