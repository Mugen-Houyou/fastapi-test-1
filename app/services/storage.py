# app/services/storage.py
import os, shutil, uuid
from pathlib import Path
from typing import cast, Tuple

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.file import FileOut
from app.crud import file as file_crud
from app.db.models.file import File

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 업로드 
def save_file(db: Session, file: UploadFile, post_id: int, uploader_id: int) -> FileOut:
    original_name: str = cast(str, file.filename)
    file_ext = Path(original_name).suffix
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = UPLOAD_DIR / unique_name

    # 디스크에 저장
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

    # 메타데이터 DB 기록 (CRUD 레이어로)
    file_meta = file_crud.create_file_meta(
        db,
        filename=original_name,
        object_key=str(file_path),
        content_type=file.content_type or "application/octet-stream",
        size=os.path.getsize(file_path),
        post_id=post_id,
        uploader_id=uploader_id,
    )

    return FileOut(
        id=file_meta.id,
        filename=file_meta.filename,
        url=f"/api/v1/files/{file_meta.id}/download",
        content_type=file_meta.content_type,
        size=file_meta.size,
        created_at=file_meta.created_at,
    )


# 스트림 반환 
def get_file_stream(db: Session, file_id: int) -> Tuple[Path, File]:
    meta = file_crud.get_file_meta(db, file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")

    path = Path(meta.object_key)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File missing on disk")

    return path, meta


# 삭제 
def delete_file(db: Session, file_id: int) -> None:
    meta = file_crud.get_file_meta(db, file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")

    # 디스크 삭제
    path = Path(meta.object_key)
    if path.exists():
        path.unlink()

    # 메타데이터 삭제 (CRUD 레이어로)
    file_crud.delete_file_meta(db, meta)
