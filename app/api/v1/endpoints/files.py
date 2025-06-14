# app/api/v1/endpoints/files.py
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.storage import save_file, get_file_stream, delete_file
from app.schemas.file import FileOut

router = APIRouter()

@router.post("/posts/{post_id}/files", response_model=FileOut, status_code=status.HTTP_201_CREATED)
def upload_file(
    post_id: int,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return save_file(db, file, post_id, current_user.id)

@router.get("/files/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file_path, file_meta = get_file_stream(db, file_id)
    return FileResponse(
        path=file_path,
        filename=file_meta.filename,
        media_type=file_meta.content_type
    )

@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_file(db, file_id)
