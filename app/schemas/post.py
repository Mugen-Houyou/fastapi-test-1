# app/schemas/post.py
"""
게시글(Post) 관련 Pydantic 스키마 정의
- PostCreate   : 게시글 생성 요청 DTO
- PostUpdate   : 게시글 수정 요청 DTO (부분 수정 허용)
- PostOut      : 게시글 단건 조회 응답 DTO
- PostListOut  : 게시글 목록 조회 응답 DTO (요약형)
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# 공통 하위 스키마 
class UserBrief(BaseModel):
    """작성자 요약 정보"""
    id: int
    username: str

    class Config:
        orm_mode = True


class FileMeta(BaseModel):
    """첨부파일 메타 정보"""
    id: int
    filename: str
    url: str

    class Config:
        orm_mode = True


# 요청(Request) 
class _PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str


class PostCreate(_PostBase):
    """게시글 생성 요청"""
    # 파일은 multipart/form-data 로 별도 업로드하므로 필드 없음
    pass


class PostUpdate(BaseModel):
    """게시글 부분 수정 요청 (모든 필드 Optional)"""
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None


# 응답(Response)
class PostOut(_PostBase):
    """게시글 단건 상세 응답"""
    id: int
    author: UserBrief
    files: List[FileMeta] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostListOut(BaseModel):
    """게시글 목록(요약) 응답"""
    id: int
    title: str
    author: UserBrief
    created_at: datetime

    class Config:
        orm_mode = True
