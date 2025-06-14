# app/schemas/comment.py

"""
댓글(Comment) · 대댓글(Reply)용 Pydantic 스키마
- CommentCreate : 댓글/대댓글 작성용 요청 DTO
- CommentUpdate : 댓글/대댓글 수정 요청 DTO
- CommentOut    : 댓글/대댓글 응답 DTO (작성자·계층 포함)
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# 재사용: 게시글 스키마에 정의된 작성자 요약 타입
from app.schemas.post import UserBrief


# ────────────────────────── 요청(Request) ──────────────────────────
class CommentCreate(BaseModel):
    """댓글/대댓글 작성 요청"""
    content: str = Field(..., min_length=1, max_length=10_000)


class CommentUpdate(BaseModel):
    """댓글/대댓글 수정 요청 (부분 수정)"""
    content: Optional[str] = Field(None, min_length=1, max_length=10_000)


# ────────────────────────── 응답(Response) ──────────────────────────
class CommentOut(BaseModel):
    """댓글/대댓글 응답"""
    id: int
    content: str
    depth: int
    parent_id: Optional[int] = None

    author: UserBrief
    created_at: datetime

    # 대댓글 트리
    replies: List["CommentOut"] = []

    class Config:
        orm_mode = True


# ―― Forward-ref 해결 ――――――――――――――――――――――――――――――――――――――――
CommentOut.update_forward_refs()
