from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db
from app.schemas.board import BoardCreate, BoardOut
from app.db.models.board import Board
from app.db.models.post import Post

router = APIRouter()


@router.post("/", response_model=BoardOut)
def create_board(payload: BoardCreate, db: Session = Depends(get_db)):
    board = Board(**payload.dict())
    db.add(board)
    db.commit()
    db.refresh(board)
    return BoardOut(
        id=board.id,
        name=board.name,
        description=board.description,
        posts=0,
        created_at=board.created_at,
    )

@router.get("/", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db)):
    results = (
        db.query(Board, func.count(Post.id).label("posts"))
        .outerjoin(Post, Board.id == Post.board_id)
        .group_by(Board.id)
        .all()
    )
    boards = []
    for board, posts in results:
        boards.append(
            BoardOut(
                id=board.id,
                name=board.name,
                description=board.description,
                posts=posts,
                created_at=board.created_at,
            )
        )
    return boards


@router.get("/all_boards", response_model=list[BoardOut])
def list_all_boards(db: Session = Depends(get_db)):
    results = (
        db.query(Board, func.count(Post.id).label("posts"))
        .outerjoin(Post, Board.id == Post.board_id)
        .group_by(Board.id)
        .all()
    )
    boards = []
    for board, posts in results:
        boards.append(
            BoardOut(
                id=board.id,
                name=board.name,
                description=board.description,
                posts=posts,
                created_at=board.created_at,
            )
        )
    return boards
