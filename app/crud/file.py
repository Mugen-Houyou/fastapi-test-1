# app/crud/file.py
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.file import File

# 생성 
def create_file_meta(
    db: Session,
    *,
    filename: str,
    object_key: str,
    content_type: str,
    size: int,
    post_id: int,
    uploader_id: int | None,
) -> File:
    meta = File(
        filename=filename,
        object_key=object_key,
        content_type=content_type,
        size=size,
        post_id=post_id,
        uploader_id=uploader_id,
    )
    db.add(meta)
    db.commit()
    db.refresh(meta)
    return meta


# 조회
def get_file_meta(db: Session, file_id: int) -> Optional[File]:
    return db.query(File).filter(File.id == file_id).first()


# 삭제
def delete_file_meta(db: Session, file: File) -> None:
    db.delete(file)
    db.commit()
