# 视频上传和访问接口
# app/video/routes.py

import os
from fastapi import APIRouter, UploadFile, Form, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.job.models import JobPost
from app.resume.models import Resume
from app.company.models import Company
from types import SimpleNamespace

from app.auth.routes import get_current_user  # 获取当前登录用户的依赖
from app.auth.models import User  # 用户模型
from app.db import get_db  # 获取数据库会话的依赖
from app.video import models, schemas, utils  # 导入视频相关模块

from app.config import settings


router = APIRouter(prefix="/video", tags=["视频模块"])  # 路由前缀和标签

VIDEO_STORAGE_DIR = settings.VIDEO_STORAGE_DIR  # 上传文件保存的相对目录，与原接口保持一致
os.makedirs(VIDEO_STORAGE_DIR, exist_ok=True)  # 如果目录不存在则自动创建

def secure_filename(filename: str) -> str:
    # 简单处理，防止目录遍历攻击，只保留文件名部分
    return os.path.basename(filename)

@router.post("/upload", response_model=schemas.VideoOut)
async def upload_video(
    title: str = Form(...),   # 视频标题
    description: str = Form(...),  # 视频描述
    # 目标类型和ID可选，用于关联其他实体（如职位、简历等）
    # 这里使用 Form 来接收表单数据
    target_type: schemas.TargetType | None = Form(None),
    target_id: str | None = Form(None),  # 目标ID 
    file: UploadFile = File(...),  # 上传的视频文件
    db: Session = Depends(get_db),  # 数据库会话依赖
    current_user: User = Depends(get_current_user)  # 当前登录用户依赖
):
    # 校验文件名和格式
    if not file.filename or not file.filename.endswith((".mp4", ".mov", ".avi")):
        raise HTTPException(400, detail="不支持的视频格式")

    file_path = await utils.save_video_file(file)  # 保存视频文件并返回保存后的文件名

    # 创建视频记录
    video = models.Video(
        title=title,
        description=description,
        file_path=file_path,
        filename=os.path.basename(file_path),  # 使用上传的文件名
        owner_id=current_user.id,
        target_type=target_type,
        target_id=target_id
    )
    db.add(video)  # 添加到数据库
    db.commit()    # 提交事务
    db.refresh(video)  # 刷新获取最新数据
    return video  # 返回视频信息


@router.get("/feed" , response_model=list[schemas.VideoOut|schemas.VideoWithTarget])
def get_video_feed(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="每页数量"),
    target_type: schemas.TargetType | None = Query(None, description="按关联类型过滤视频"), 
):
    # 1. 基础查询：查询视频表
    query = db.query(models.Video)

    # 2. 如果传递了target_type，添加过滤条件
    if target_type:
        query = query.filter(models.Video.target_type == target_type)
        
    # 3. 排序、分页
    videos = (
        query
        .order_by(models.Video.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    # 添加上传者信息

    result = []
    for video in videos:
        target_summary = None
        
        # 根据不同的target_type关联相应的业务对象
        if video.target_type == schemas.TargetType.job and video.target_id:
            job = db.query(JobPost).filter(JobPost.id == video.target_id).first()
            if job:
                target_summary = {
                    "id": job.id,
                    "title": job.title,
                    "location": job.location,
                    "salary_min": job.salary_min,
                    "salary_max": job.salary_max,
                }
        elif video.target_type == schemas.TargetType.resume and video.target_id:
            resume = db.query(Resume).filter(Resume.id == video.target_id).first()
            if resume:
                target_summary = {
                    "id": resume.id,
                    "title": resume.title,
                    "experience_years": resume.experience_years,
                    "skills": resume.skills.split(",") if resume.skills else [],
                    "major": resume.major,
                }
        elif video.target_type == schemas.TargetType.company_intro and video.target_id:
            company = db.query(Company).filter(Company.id == video.target_id).first()
            if company:
                target_summary = {
                    "id": company.id,
                    "name": company.name,
                    "industry": company.industry,
                    "location": company.location,
                }
        
        # 构建返回数据
        result.append(
            schemas.VideoWithTarget(
                id=video.id,
                title=video.title,
                filename=video.filename,
                description=video.description,
                file_path=video.file_path,
                cover_path=video.cover_path,
                created_at=video.created_at,
                upload_time=video.upload_time,
                owner_username=video.owner.username if video.owner else "unknown",
                target_type=video.target_type,
                target_id=video.target_id,
                target_summary=target_summary
            )
        )
    return result

