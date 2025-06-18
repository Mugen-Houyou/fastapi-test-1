from datetime import datetime
from pydantic import BaseModel

class BoardBase(BaseModel):
    name: str
    description: str | None = None

class BoardCreate(BoardBase):
    pass

class BoardOut(BoardBase):
    id: int
    posts: int
    created_at: datetime
    room_name: str

    class Config:
        from_attributes = True
