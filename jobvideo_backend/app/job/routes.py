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

# 获取所有职位列表（增加一个与原接口兼容的路由）
@router.get("/", response_model=List[schemas.JobPostOut])
def list_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.JobPost).filter(models.JobPost.status == "open").all()
    return jobs

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

# 更新职位（仅雇主可更新自己发布的职位）
@router.put("/{job_id}", response_model=schemas.JobPostOut)
def update_job(
    job_id: int,
    job: schemas.JobPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
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

# 删除职位（仅雇主可删除自己发布的职位）
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.employer))
):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_id).first()
    if not job_post:
        raise HTTPException(status_code=404, detail="职位不存在")
    
    # 确保只有职位发布者可以删除
    if job_post.employer_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此职位")
    
    db.delete(job_post)
    db.commit()
    return {"message": "职位删除成功"}
