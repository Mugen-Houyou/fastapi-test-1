from datetime import datetime
from pydantic import BaseModel

class BoardBase(BaseModel):
    name: str
    description: str | None = None

class BoardCreate(BoardBase):
    pass

class BoardOut(BoardBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
