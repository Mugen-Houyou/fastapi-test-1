# app/api/v1/endpoints/files.py
from fastapi import APIRouter, Depends, File, UploadFile, status, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
# from app.schemas.file import FileOut
# from app.services.storage import upload_file, stream_file, delete_file_by_id

router = APIRouter()

# @router.post("/posts/{post_id}/files", response_model=FileOut, status_code=status.HTTP_201_CREATED)
# def upload_post_file(
#     post_id: int,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     return upload_file(db, post_id, file, current_user.id)

# @router.get("/files/{file_id}/download")
# def download_file(file_id: int, db: Session = Depends(get_db)):
#     stream, filename = stream_file(db, file_id)
#     return StreamingResponse(stream, headers={"Content-Disposition": f"attachment; filename={filename}"})

# @router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
# def remove_file(
#     file_id: int = Path(..., gt=0),
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     delete_file_by_id(db, file_id, current_user.id)
