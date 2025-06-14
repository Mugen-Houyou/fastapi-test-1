# app/services/storage.py
"""
향후 파일 저장소를 AWS S3이나 Azure Blob 등 클라우드로 옮길 때, 이 app/services/storage.py만 바꿔끼우면 됨.
"""

import os
import shutil
import uuid
from typing import cast
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.file import File
from app.db.models.user import User
from app.schemas.file import FileOut

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(
    db: Session,
    file: UploadFile,
    post_id: int,
    uploader_id: int,
) -> FileOut:
    """
    파일 저장 및 메타데이터를 DB에 기록
    """
    # 고유 파일명
    original_name: str = cast(str, file.filename)

    file_ext = Path(original_name).suffix
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_location = UPLOAD_DIR / unique_filename

    # 디스크에 파일 저장
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

    # 메타데이터를 DB에 기록
    file_meta = File(
        filename=file.filename,
        object_key=str(file_location),
        content_type=file.content_type,
        size=os.path.getsize(file_location),
        post_id=post_id,
        uploader_id=uploader_id,
    )
    db.add(file_meta)
    db.commit()
    db.refresh(file_meta)
    # file_url = f"/api/v1/files/{file_meta.id}/download"
    return FileOut(
        id=file_meta.id,
        filename=file_meta.filename,
        # url=file_url,
        content_type=file_meta.content_type,
        size=file_meta.size,
        created_at=file_meta.created_at,
    )
    # return file_meta

def get_file_stream(db: Session, file_id: int) -> tuple[Path, File]:
    """
    파일 스트림 및 메타데이터 제공
    """
    file_meta = db.query(File).filter(File.id == file_id).first()
    if not file_meta or not Path(file_meta.object_key).exists():
        raise HTTPException(status_code=404, detail="File not found")
    return Path(file_meta.object_key), file_meta

def delete_file(db: Session, file_id: int) -> None:
    """
    파일 삭제 (디스크 + DB)
    """
    file_meta = db.query(File).filter(File.id == file_id).first()
    if not file_meta:
        raise HTTPException(status_code=404, detail="File not found")

    # 파일 삭제
    file_path = Path(file_meta.object_key)
    if file_path.exists():
        file_path.unlink()

    # DB 삭제
    db.delete(file_meta)
    db.commit()
