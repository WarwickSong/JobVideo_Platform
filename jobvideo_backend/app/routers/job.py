# app/routers/job.py

from fastapi import APIRouter, HTTPException
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["Job"])

# 模拟数据库，使用字典存储职位信息
fake_db = {}
next_id = 1  # 用于生成职位ID的自增变量

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate):
    # 创建新职位接口
    global next_id
    job_id = next_id  # 分配新的职位ID
    next_id += 1
    fake_db[job_id] = job  # 保存职位信息到“数据库”
    return JobResponse(id=job_id, **job.model_dump())  # 返回创建的职位信息

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int):
    # 获取指定ID的职位信息
    job = fake_db.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")  # 未找到则返回404
    return JobResponse(id=job_id, **job.model_dump())  # 返回职位信息

@router.get("/", response_model=list[JobResponse])
def list_jobs():
    # 获取所有职位列表
    return [JobResponse(id=jid, **j.model_dump()) for jid, j in fake_db.items()]

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobCreate):
    # 更新指定ID的职位信息
    if job_id not in fake_db:
        raise HTTPException(status_code=404, detail="职位不存在")  # 未找到则返回404
    fake_db[job_id] = job  # 更新职位信息
    return JobResponse(id=job_id, **job.model_dump())  # 返回更新后的职位信息

@router.delete("/{job_id}")
def delete_job(job_id: int):
    # 删除指定ID的职位
    if job_id not in fake_db:
        raise HTTPException(status_code=404, detail="职位不存在")  # 未找到则返回404
    del fake_db[job_id]  # 从“数据库”中删除职位
    return {"message": "职位删除成功"}  # 返回删除成功消息
