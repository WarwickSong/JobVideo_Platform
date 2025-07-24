# 视频上传和访问接口
# app/video/routes.py

from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException
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
