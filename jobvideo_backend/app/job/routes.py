# app/job/routes.py
# 短视频招聘平台后端 - 职位模块路由
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.job import models, schemas
from app.auth.routes import get_current_user
from app.auth.models import User, UserRole
from app.auth.deps import role_required

router = APIRouter(prefix="/job", tags=["职位模块"])

# 发布职位（仅 employer）
@router.post("/post", response_model=schemas.JobPostOut)
def post_job(
    job: schemas.JobPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
    job_post = models.JobPost(**job.dict(), employer_id=current_user.id)
    db.add(job_post)
    db.commit()
    db.refresh(job_post)
    return job_post

# 职位列表查询（分页 + 关键词搜索）
@router.get("/list", response_model=List[schemas.JobPostOut])
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    keyword: Optional[str] = Query(None, description="关键词搜索")
):
    query = db.query(models.JobPost).filter(models.JobPost.status == "open")
    if keyword:
        query = query.filter(models.JobPost.title.ilike(f"%{keyword}%"))
    jobs = query.offset(skip).limit(limit).all()
    return jobs

# 职位详情
@router.get("/{job_id}", response_model=schemas.JobPostOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobPost).filter(models.JobPost.id == job_id).first()
    if not job:
        raise HTTPException(404, detail="职位不存在")
    return job
