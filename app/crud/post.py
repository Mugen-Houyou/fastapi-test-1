# app/crud/post.py

"""
게시글(Post) CRUD 레이어

엔드포인트(service)단에서 호출하여 DB 접근 세부 로직을 분리·재사용하도록 함
권한 체크(작성자·관리자 여부)도 이곳에서 수행
"""

from typing import List, Sequence

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.models.post import Post
from app.db.models.user import User
from app.db.models.file import File


# 조회 ~~
def get_posts_by_board(db: Session, board_id: int, page: int = 1, size: int = 10):
    offset = (page - 1) * size
    return (
        db.query(Post)
        .filter(Post.board_id == board_id)
        .order_by(desc(Post.created_at))
        .offset(offset)
        .limit(size)
        .all()
    )

def get_posts(db: Session, page: int = 1, size: int = 10) -> Sequence[Post]:
    """
    게시글 목록 조회 (기본: 최신순)
    """
    offset: int = (page - 1) * size
    return (
        db.query(Post)
        .order_by(desc(Post.created_at))
        .offset(offset)
        .limit(size)
        .all()
    )


def get_post(db: Session, post_id: int) -> Post:
    """
    게시글 단건 조회
    """
    post: Post | None = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found",
        )
    return post
# ~~ 조회

# 생성 ~~
def create_post(db: Session, payload, author_id: int) -> Post:
    """
    게시글 생성
    """
    post = Post(
        title=payload.title,
        content=payload.content,
        author_id=author_id,
        board_id=payload.board_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
# ~~ 생성

# 수정 ~~
def update_post(db: Session, post_id: int, payload, requester_id: int) -> Post:
    """
    게시글 수정 – 작성자 본인 또는 관리자만 허용
    """
    post = get_post(db, post_id)  # 404 처리 내장

    _authorize(post, requester_id)

    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content
    if payload.board_id is not None:
        post.board_id = payload.board_id

    db.commit()
    db.refresh(post)
    return post
# ~~ 수정


# 삭제 ~~
def delete_post(db: Session, post_id: int, requester_id: int) -> None:
    """
    게시글 삭제 - 작성자 본인 또는 관리자만 허용
    """
    post = get_post(db, post_id)  # 404 처리 내장

    _authorize(post, requester_id)

    db.delete(post)
    db.commit()
# ~~ 삭제


# 내부 헬퍼 ~~
def _authorize(post: Post, requester_id: int) -> None:
    """
    작성자 본인 또는 관리자 권한 확인
    """
    if post.author_id == requester_id:
        return

    # 관리자 여부 확인
    user: User | None = post.author  # lazy-loaded 관계로부터 Author 객체
    if user is None or not getattr(user, "is_admin", False): # TODO: 현재 admin만 허용 가능 - 작성자도 할 수 있도록!!
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this post",
        )
# ~~ 내부 헬퍼 
