# app/job/routes.py
# 短视频招聘平台后端 - 职位模块路由
# 功能：实现职位发布、查询、更新和删除等API接口

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.job import models, schemas
from app.auth.routes import get_current_user
from app.auth.models import User, UserRole
from app.auth.deps import role_required

router = APIRouter(prefix="/job", tags=["职位模块"])


@router.post("/post", response_model=schemas.JobPostOut)
def post_job(
    job: schemas.JobPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
    """
    发布职位接口：
        雇主发布新的职位信息
    
    Args:
        job: 职位信息
        db: 数据库会话
        current_user: 当前登录用户（必须是雇主）
    
    Returns:
        JobPostOut: 发布成功的职位信息
    """
    job_post = models.JobPost(**job.dict(), employer_id=current_user.id)
    db.add(job_post)
    db.commit()
    db.refresh(job_post)
    return job_post


@router.get("/", response_model=List[schemas.JobPostOut])
def list_all_jobs(db: Session = Depends(get_db)):
    """
    获取所有职位列表接口：
        返回所有开放的职位列表（与原接口兼容）
    
    Args:
        db: 数据库会话
    
    Returns:
        List[JobPostOut]: 所有开放的职位列表
    """
    jobs = db.query(models.JobPost).filter(models.JobPost.status == "open").all()
    return jobs


@router.get("/list", response_model=List[schemas.JobPostOut])
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    keyword: Optional[str] = Query(None, description="关键词搜索")
):
    """
    职位列表查询接口：
        支持分页和关键词搜索的职位列表查询
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数（分页用）
        limit: 每页记录数
        keyword: 关键词搜索（可选）
    
    Returns:
        List[JobPostOut]: 职位列表
    """
    query = db.query(models.JobPost).filter(models.JobPost.status == "open")
    if keyword:
        query = query.filter(models.JobPost.title.ilike(f"%{keyword}%"))
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=schemas.JobPostOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    获取职位详情接口：
        返回指定职位的详细信息
    
    Args:
        job_id: 职位ID
        db: 数据库会话
    
    Returns:
        JobPostOut: 职位详细信息
    
    Raises:
        HTTPException: 当职位不存在时抛出404错误
    """
    job = db.query(models.JobPost).filter(models.JobPost.id == job_id).first()
    if not job:
        raise HTTPException(404, detail="职位不存在")
    return job


@router.put("/{job_id}", response_model=schemas.JobPostOut)
def update_job(
    job_id: int,
    job: schemas.JobPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
    """
    更新职位接口：
        雇主更新自己发布的职位信息
    
    Args:
        job_id: 职位ID
        job: 更新的职位信息
        db: 数据库会话
        current_user: 当前登录用户（必须是雇主）
    
    Returns:
        JobPostOut: 更新后的职位信息
    
    Raises:
        HTTPException: 当职位不存在或无权更新时抛出404或403错误
    """
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_id).first()
    if not job_post:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    # 确保只有职位发布者可以更新
    if job_post.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权更新此职位")
    
    # 更新职位信息
    for key, value in job.dict().items():
        setattr(job_post, key, value)
    
    db.commit()
    db.refresh(job_post)
    return job_post


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
    """
    删除职位接口：
        雇主删除自己发布的职位
    
    Args:
        job_id: 职位ID
        db: 数据库会话
        current_user: 当前登录用户（必须是雇主）
    
    Returns:
        dict: 删除成功的消息
    
    Raises:
        HTTPException: 当职位不存在或无权删除时抛出404或403错误
    """
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_id).first()
    if not job_post:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    # 确保只有职位发布者可以删除
    if job_post.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此职位")
    
    db.delete(job_post)
    db.commit()
    return {"message": "职位删除成功"}
