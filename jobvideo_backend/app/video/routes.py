# app/video/routes.py
# 视频上传和访问接口
# 功能：实现视频上传、视频列表和视频详情等API接口

import os
from fastapi import APIRouter, UploadFile, Form, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from types import SimpleNamespace

from app.auth.routes import get_current_user, get_current_user_optional  # 获取当前登录用户的依赖
from app.auth.models import User  # 用户模型
from app.db import get_db  # 获取数据库会话的依赖
from app.video import models, schemas, utils, resolvers  # 导入视频相关模块
from app.interactions.models import VideoLike, VideoFavorite  # 交互行为模型

from app.config import settings

# 创建路由器
# 前缀设置为"/video"，表示所有接口都以"/video"开头
# 标签设置为"视频模块"，用于API文档分类
router = APIRouter(prefix="/video", tags=["视频模块"])

VIDEO_STORAGE_DIR = settings.VIDEO_STORAGE_DIR  # 上传文件保存的相对目录，与原接口保持一致
os.makedirs(VIDEO_STORAGE_DIR, exist_ok=True)  # 如果目录不存在则自动创建


def secure_filename(filename: str) -> str:
    """
    安全文件名处理函数：
        防止目录遍历攻击，只保留文件名部分
    
    Args:
        filename: 原始文件名
    
    Returns:
        str: 处理后的安全文件名
    """
    return os.path.basename(filename)


@router.post("/upload", response_model=schemas.VideoOut)
async def upload_video(
    title: str = Form(...),   # 视频标题
    description: str = Form(...),  # 视频描述
    target_type: schemas.TargetType | None = Form(None),  # 目标类型
    target_id: str | None = Form(None),  # 目标ID
    file: UploadFile = File(...),  # 上传的视频文件
    db: Session = Depends(get_db),  # 数据库会话依赖
    current_user: User = Depends(get_current_user)  # 当前登录用户依赖
):
    """
    视频上传接口：
        用户上传视频并保存到数据库
    
    Args:
        title: 视频标题
        description: 视频描述
        target_type: 目标类型（可选），用于关联其他实体（如职位、简历等）
        target_id: 目标ID（可选）
        file: 上传的视频文件
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        VideoOut: 上传成功的视频信息
    
    Raises:
        HTTPException: 当文件格式不支持时抛出400错误
    """
    # 校验文件名和格式
    if not file.filename or not file.filename.endswith((".mp4", ".mov", ".avi")):
        raise HTTPException(400, detail="不支持的视频格式")

    file_path = await utils.save_video_file(file)  # 保存视频文件并返回保存后的文件名

    # 改为完整URL
    file_path_url = f"/videos/{os.path.basename(file_path)}"
    
    # 创建视频记录
    video = models.Video(
        title=title,
        description=description,
        file_path=file_path_url,  # 使用完整URL
        filename=os.path.basename(file_path),  # 使用上传的文件名
        owner_id=current_user.id,
        target_type=target_type,
        target_id=target_id
    )
    db.add(video)  # 添加到数据库
    db.commit()    # 提交事务
    db.refresh(video)  # 刷新获取最新数据
    return video  # 返回视频信息


@router.get("/feed", response_model=list[schemas.VideoOut | schemas.VideoWithTarget])
def get_video_feed(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(10, ge=1, le=50, description="每页数量"),
    target_type: schemas.TargetType | None = Query(None, description="按关联类型过滤视频"),
    owner_role: str | None = Query(None, description="按上传者角色过滤视频（seeker / employer）"),
    current_user: User | None = Depends(get_current_user_optional)  # 可选的当前用户
):
    """
    获取视频列表接口：
        返回视频列表，支持分页和按目标类型过滤
        使用批量查询优化，避免 N+1 查询问题
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数（分页用）
        limit: 每页记录数
        target_type: 目标类型过滤条件（可选）
        owner_role: 上传者角色过滤条件（可选，seeker/employer）
        current_user: 可选的当前用户（支持未登录）
    
    Returns:
        list[VideoOut | VideoWithTarget]: 视频列表，包含视频信息和关联的目标对象摘要
    """
    # Step 1: 基础查询：从视频表关联用户表
    query = db.query(models.Video).join(User, models.Video.owner_id == User.id)

    # Step 2: 如果传递了target_type，添加过滤条件
    if target_type:
        query = query.filter(models.Video.target_type == target_type)

    # Step 3: 如果传递了owner_role，按上传者角色过滤
    if owner_role:
        query = query.filter(User.role == owner_role)
        
    # Step 3: 排序、分页
    videos = (
        query
        .order_by(models.Video.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Step 4: 提取当前页的视频ID列表
    video_ids = [v.id for v in videos]
    
    # Step 5: 批量查询点赞数（使用 group by 聚合）
    like_counts = (
        db.query(
            VideoLike.video_id,
            func.count(VideoLike.id)
        )
        .filter(VideoLike.video_id.in_(video_ids))
        .group_by(VideoLike.video_id)
        .all()
    )
    # 构建点赞数字典映射
    like_count_map = {vid: count for vid, count in like_counts}
    
    # Step 6: 批量查询收藏数（使用 group by 聚合）
    favorite_counts = (
        db.query(
            VideoFavorite.video_id,
            func.count(VideoFavorite.id)
        )
        .filter(VideoFavorite.video_id.in_(video_ids))
        .group_by(VideoFavorite.video_id)
        .all()
    )
    # 构建收藏数字典映射
    favorite_count_map = {vid: count for vid, count in favorite_counts}
    
    # Step 7: 批量查询当前用户的点赞状态
    liked_video_ids = set()
    if current_user:
        liked_rows = (
            db.query(VideoLike.video_id)
            .filter(
                VideoLike.video_id.in_(video_ids),
                VideoLike.user_id == current_user.id
            )
            .all()
        )
        liked_video_ids = {row[0] for row in liked_rows}
    
    # Step 8: 批量查询当前用户的收藏状态
    favorited_video_ids = set()
    if current_user:
        favorited_rows = (
            db.query(VideoFavorite.video_id)
            .filter(
                VideoFavorite.video_id.in_(video_ids),
                VideoFavorite.user_id == current_user.id
            )
            .all()
        )
        favorited_video_ids = {row[0] for row in favorited_rows}
    
    # Step 9: 批量查询目标对象信息（避免 N+1 问题）
    target_info_map = {}
    target_video_ids = [(v.target_type, v.target_id) for v in videos if v.target_type and v.target_id]
    
    # 按目标类型分组
    job_ids = [tid for ttype, tid in target_video_ids if ttype == schemas.TargetType.job]
    resume_ids = [tid for ttype, tid in target_video_ids if ttype == schemas.TargetType.resume]
    company_ids = [tid for ttype, tid in target_video_ids if ttype == schemas.TargetType.company_intro]
    
    # 批量查询职位信息
    from app.job.models import JobPost
    job_map = {}
    if job_ids:
        jobs = db.query(JobPost).filter(JobPost.id.in_(job_ids)).all()
        job_map = {job.id: job for job in jobs}
    
    # 批量查询简历信息
    from app.resume.models import Resume
    resume_map = {}
    if resume_ids:
        resumes = db.query(Resume).filter(Resume.id.in_(resume_ids)).all()
        resume_map = {resume.id: resume for resume in resumes}
    
    # 批量查询公司信息
    from app.company.models import Company
    company_map = {}
    if company_ids:
        companies = db.query(Company).filter(Company.id.in_(company_ids)).all()
        company_map = {company.id: company for company in companies}
    
    # Step 10: 组装返回数据
    result = []
    for video in videos:
        target_summary = None
        
        # 使用预查询的目标对象信息
        if video.target_type and video.target_id:
            if video.target_type == schemas.TargetType.job and video.target_id in job_map:
                job = job_map[video.target_id]
                target_summary = {
                    "id": job.id,
                    "title": job.title,
                    "location": job.location,
                    "salary_min": job.salary_min,
                    "salary_max": job.salary_max,
                }
            elif video.target_type == schemas.TargetType.resume and video.target_id in resume_map:
                resume = resume_map[video.target_id]
                target_summary = {
                    "id": resume.id,
                    "title": resume.title,
                    "experience_years": resume.experience_years,
                    "skills": resume.skills.split(",") if resume.skills else [],
                    "major": resume.major,
                }
            elif video.target_type == schemas.TargetType.company_intro and video.target_id in company_map:
                company = company_map[video.target_id]
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
                owner_role=video.owner.role.value if video.owner else None,
                target_type=video.target_type,
                target_id=video.target_id,
                target_summary=target_summary,
                like_count=int(like_count_map.get(video.id, 0)),
                favorite_count=int(favorite_count_map.get(video.id, 0)),
                is_liked_by_me=bool(video.id in liked_video_ids),
                is_favorited_by_me=bool(video.id in favorited_video_ids)
            )
        )
    return result


@router.get("/{video_id}", response_model=schemas.VideoDetail)
def get_video_detail(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)  # 可选的当前用户
):
    """
    获取视频详情接口：
        返回指定视频的详细信息，包括关联的目标对象和交互数据
    
    Args:
        video_id: 视频ID
        db: 数据库会话
        current_user: 可选的当前用户（支持未登录）
    
    Returns:
        VideoDetail: 视频详细信息，包含关联的目标对象和交互数据
    
    Raises:
        HTTPException: 当视频不存在时抛出404错误
    """
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")

    target = None

    # 如果视频有关联的目标对象，解析目标对象信息
    if video.target_type and video.target_id:
        target = resolvers.resolve_target(
            target_type=video.target_type,
            target_id=video.target_id,
            db=db
        )

    # 查询点赞数
    like_count = db.query(VideoLike).filter(VideoLike.video_id == video_id).count()
    
    # 查询收藏数
    favorite_count = db.query(VideoFavorite).filter(VideoFavorite.video_id == video_id).count()
    
    # 查询当前用户是否点赞
    is_liked_by_me = False
    if current_user:
        is_liked_by_me = db.query(VideoLike).filter(
            VideoLike.video_id == video_id,
            VideoLike.user_id == current_user.id
        ).first() is not None
    
    # 查询当前用户是否收藏
    is_favorited_by_me = False
    if current_user:
        is_favorited_by_me = db.query(VideoFavorite).filter(
            VideoFavorite.video_id == video_id,
            VideoFavorite.user_id == current_user.id
        ).first() is not None

    return {
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "file_path": video.file_path,
        "filename": video.filename,
        "cover_path": video.cover_path,
        "created_at": video.created_at,
        "upload_time": video.upload_time,
        "owner_username": video.owner.username if video.owner else "unknown",
        "target": target,
        "like_count": int(like_count),
        "favorite_count": int(favorite_count),
        "is_liked_by_me": bool(is_liked_by_me),
        "is_favorited_by_me": bool(is_favorited_by_me)
    }
