# app/api/v1/endpoints/comments.py
from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut
from app.api.deps import get_db, get_current_user
from app.crud import comment as comment_crud

router = APIRouter()


# 댓글 ~~

@router.get("/posts/{post_id}/comments", response_model=List[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_crud.get_comments_by_post(db, post_id)

@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return comment_crud.create_comment(db, post_id, payload, current_user.id)

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return comment_crud.update_comment(db, comment_id, payload, current_user.id)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment_crud.delete_comment(db, comment_id, current_user.id)

# ~~ 댓글

# 대댓글 ~~
# TODO: Nested의 레벨 몇까지 제한할지??

@router.get("/comments/{comment_id}/replies", response_model=List[CommentOut])
def list_replies(comment_id: int, db: Session = Depends(get_db)):
    return comment_crud.get_replies(db, comment_id)

@router.post("/comments/{comment_id}/replies", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_reply(
    comment_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return comment_crud.create_reply(db, comment_id, payload, current_user.id)

# ~~ 대댓글