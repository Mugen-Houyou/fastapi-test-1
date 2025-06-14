from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.board import BoardCreate, BoardOut
from app.db.models.board import Board

router = APIRouter()

@router.post("/", response_model=BoardOut)
def create_board(payload: BoardCreate, db: Session = Depends(get_db)):
    board = Board(**payload.dict())
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

@router.get("/", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db)):
    return db.query(Board).all()
