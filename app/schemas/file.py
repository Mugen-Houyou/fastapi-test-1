# app/schemas/file.py
"""
파일(File) 관련 Pydantic 스키마 정의
- FileOut : 파일 조회 응답 DTO
"""

from datetime import datetime
from pydantic import BaseModel

class FileOut(BaseModel):
    id: int
    filename: str
    url: str
    content_type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True
