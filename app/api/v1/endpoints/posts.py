# app/api/v1/endpoints/posts.py
from typing import List, Any
from fastapi import APIRouter, Depends, Path, Query, UploadFile, File, status
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostUpdate, PostOut, PostListOut
from app.api.deps import get_db, get_current_user, get_current_admin
from app.crud import post as post_crud

router = APIRouter()


@router.get("/all_posts", response_model=List[PostListOut])
def list_posts_all(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: Session = Depends(get_db),
    _: Any = Depends(get_current_admin),   # 관리자 권한 체크용 dependency (전체 게시글은 관리자만 확인 가능하도록)
):
    return post_crud.get_posts(db, page, size)

@router.get("/boards/{board_id}/posts", response_model=List[PostListOut])
def list_posts_by_board(
    board_id: int = Path(..., gt=0),
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return post_crud.get_posts_by_board(db, board_id, page, size)

@router.get("/boards/{board_id}/posts/{post_id}", response_model=PostOut)
def read_post(post_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return post_crud.get_post(db, post_id)

@router.post("/boards/{board_id}/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return post_crud.create_post(db, payload, current_user.id)

@router.put("/boards/{board_id}/posts/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return post_crud.update_post(db, post_id, payload, current_user.id)

@router.delete("/boards/{board_id}/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post_crud.delete_post(db, post_id, current_user.id)
