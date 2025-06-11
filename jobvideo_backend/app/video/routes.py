# 视频上传和访问接口
# app/video/routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user
from app.auth.models import User
from app.db import get_db
from app.video import models, schemas, utils

router = APIRouter(prefix="/video", tags=["视频模块"])

@router.post("/upload", response_model=schemas.VideoOut)
def upload_video(
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename or not file.filename.endswith((".mp4", ".mov", ".avi")):
        raise HTTPException(400, detail="不支持的视频格式")

    saved_name = utils.save_video_file(file)

    video = models.Video(
        title=title,
        filename=saved_name,
        owner_id=current_user.id
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video
