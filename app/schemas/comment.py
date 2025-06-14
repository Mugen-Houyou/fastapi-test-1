# app/schemas/comment.py
"""
댓글(Comment) & 대댓글(Reply)용 Pydantic 스키마 정의
- CommentCreate : 댓글/대댓글 작성용 요청 DTO. content 필드에 댓글 내용을 입력받으며, 길이는 1~10000자까지 허용 
- CommentUpdate : 댓글/대댓글 수정 요청 DTO. content 필드는 선택적(Optional)이며, 부분 수정(Patch) 요청에 사용
- CommentOut    : 댓글/대댓글 응답 DTO (작성자·계층 포함).  
    댓글의 id, 내용(content), 계층(depth), 부모 댓글 id(parent_id), 작성자(author), 생성일시(created_at), 그리고 대댓글 리스트(replies)를 포함합니다. replies 필드는 자기 자신(CommentOut)의 리스트로, 대댓글 트리 구조를 표현합니다.

기타:
- UserBrief: 댓글 작성자 정보를 요약해서 담는 타입으로, 게시글 스키마에서 import하여 재사용.
- CommentOut 클래스는 Pydantic의 orm_mode를 활성화하여 ORM 객체와의 호환성을 지원.
- 자기 참조 타입(대댓글 트리)을 위해 forward reference를 사용하며, update_forward_refs()로 이를 해결.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# 재사용: 게시글 스키마에 정의된 작성자 요약 타입
from app.schemas.post import UserBrief


# 요청(Request) ~~
class CommentCreate(BaseModel):
    """댓글/대댓글 작성 요청"""
    content: str = Field(..., min_length=1, max_length=10_000)


class CommentUpdate(BaseModel):
    """댓글/대댓글 수정 요청 (부분 수정)"""
    content: Optional[str] = Field(None, min_length=1, max_length=10_000)
# ~~ 요청(Request)


# 응답(Response) ~~
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
# ~~ 응답(Response) 


# Forward-ref 관련
CommentOut.update_forward_refs()