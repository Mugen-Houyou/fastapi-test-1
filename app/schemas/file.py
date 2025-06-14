# app/schemas/file.py

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
        orm_mode = True
