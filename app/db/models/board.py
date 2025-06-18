# app/db/models/board.py
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.post import Post

class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    # 관계 
    posts: Mapped[List["Post"]] = relationship( # 관계: 1개의 보드에 n개의 포스트
        "Post",
        back_populates="board",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Board id={self.id} name={self.name!r}>"

    @property
    def room_name(self) -> str:
        """Room name for WebSocket chat."""
        return f"board_id_{self.id}"
