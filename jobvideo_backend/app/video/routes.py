# 视频上传和访问接口
# app/video/routes.py

from fastapi import APIRouter, UploadFile, Form, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.auth.routes import get_current_user  # 获取当前登录用户的依赖
from app.auth.models import User  # 用户模型
from app.db import get_db  # 获取数据库会话的依赖
from app.video import models, schemas, utils  # 导入视频相关模块


router = APIRouter(prefix="/video", tags=["视频模块"])  # 路由前缀和标签

@router.post("/upload", response_model=schemas.VideoOut)
def upload_video(
    title: str = Form(...),   # 视频标题
    file: UploadFile = File(...),  # 上传的视频文件
    db: Session = Depends(get_db),  # 数据库会话依赖
    current_user: User = Depends(get_current_user)  # 当前登录用户依赖
):
    # 校验文件名和格式
    if not file.filename or not file.filename.endswith((".mp4", ".mov", ".avi")):
        raise HTTPException(400, detail="不支持的视频格式")

    saved_name = utils.save_video_file(file)  # 保存视频文件并返回保存后的文件名

    # 创建视频记录
    video = models.Video(
        title=title,
        filename=saved_name,
        owner_id=current_user.id
    )
    db.add(video)  # 添加到数据库
    db.commit()    # 提交事务
    db.refresh(video)  # 刷新获取最新数据
    return video  # 返回视频信息


@router.get("/feed" , response_model=list[schemas.VideoOut])
def get_video_feed(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="每页数量"),
):

    videos = (
        db.query(models.Video)
        .order_by(models.Video.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    # 添加上传者信息
    result = [
        schemas.VideoOut(
            id=video.id,
            title=video.title,
            filename=video.filename,
            description=video.description,
            file_path=video.file_path,
            cover_path=video.cover_path,
            created_at=video.created_at,
            upload_time=video.upload_time,
            owner_username=video.owner.username if video.owner else "unknown",
        )
        for video in videos
    ]
    return result

