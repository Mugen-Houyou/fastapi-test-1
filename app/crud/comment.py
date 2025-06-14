# app/crud/comment.py

"""
댓글(Comment) & 대댓글(Reply) CRUD 레이어

- 게시글(Post) 1:N
- 자기 참조(parent/children) 트리
- 작성자 본인 또는 관리자 권한 확인
"""

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.db.models.comment import Comment
from app.db.models.post import Post
from app.db.models.user import User


# ────────────────────────── 조회 ──────────────────────────
def get_comments_by_post(db: Session, post_id: int) -> Sequence[Comment]:
    """
    특정 게시글의 **최상위 댓글** 목록 조회 (대댓글 제외)
    """
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.parent_id.is_(None))
        .order_by(asc(Comment.created_at))
        .all()
    )


def get_replies(db: Session, parent_id: int) -> Sequence[Comment]:
    """
    특정 댓글의 대댓글 목록 조회
    """
    return (
        db.query(Comment)
        .filter(Comment.parent_id == parent_id)
        .order_by(asc(Comment.created_at))
        .all()
    )


def _get_comment_or_404(db: Session, comment_id: int) -> Comment:
    """
    내부 헬퍼: 댓글 없으면 404
    """
    comment: Comment | None = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment {comment_id} not found",
        )
    return comment


# ────────────────────────── 생성 ──────────────────────────
def create_comment(db: Session, post_id: int, payload, author_id: int) -> Comment:
    """
    게시글에 **최상위 댓글** 생성
    """
    # 게시글 존재 확인
    if not db.query(Post.id).filter(Post.id == post_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found",
        )

    comment = Comment(
        content=payload.content,
        post_id=post_id,
        author_id=author_id,
        depth=0,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def create_reply(db: Session, parent_id: int, payload, author_id: int) -> Comment:
    """
    **대댓글** 생성
    """
    parent = _get_comment_or_404(db, parent_id)

    reply = Comment(
        content=payload.content,
        post_id=parent.post_id,
        author_id=author_id,
        parent_id=parent.id,
        depth=parent.depth + 1,
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return reply


# ────────────────────────── 수정 ──────────────────────────
def update_comment(db: Session, comment_id: int, payload, requester_id: int) -> Comment:
    """
    댓글/대댓글 수정 – 작성자 본인 또는 관리자만 허용
    """
    comment = _get_comment_or_404(db, comment_id)
    _authorize(comment, requester_id)

    if payload.content is not None:
        comment.content = payload.content

    db.commit()
    db.refresh(comment)
    return comment


# ────────────────────────── 삭제 ──────────────────────────
def delete_comment(db: Session, comment_id: int, requester_id: int) -> None:
    """
    댓글/대댓글 삭제 – 작성자 본인 또는 관리자만 허용
    """
    comment = _get_comment_or_404(db, comment_id)
    _authorize(comment, requester_id)

    db.delete(comment)
    db.commit()


# ────────────────────────── 내부 권한 헬퍼 ──────────────────────────
def _authorize(comment: Comment, requester_id: int) -> None:
    """
    작성자 본인 또는 관리자 권한 확인
    """
    if comment.author_id == requester_id:
        return

    user: User | None = comment.author
    if user is None or not getattr(user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this comment",
        )
