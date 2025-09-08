# Pydantic 请求/响应模型
# app/video/schemas.py

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.video.models import TargetType


class JobSummary(BaseModel):
    id: int
    title: str
    location: str
    salary_min: int
    salary_max: int


class ResumeSummary(BaseModel):
    id: int
    title: str
    skills: list[str]  # 举例


class CompanyIntroSummary(BaseModel):
    id: int
    name: str
    industry: str


class VideoWithTarget(BaseModel):
    id: int
    title: str
    filename: str
    description: str
    file_path: str
    cover_path: str | None
    created_at: datetime
    upload_time: datetime
    owner_username: str
    target_type: TargetType | None
    target_id: int | None
    target_summary: dict | None  # 由后端构造 

    class Config:
        from_attributes = True


class VideoBase(BaseModel):
    title: str  # 视频标题


class VideoCreate(VideoBase):
    # 创建视频时使用的请求体，继承基础模型
    title: str
    description: str
    target_type: TargetType | None = None
    target_id: int | None = None


class VideoOut(BaseModel):
    id: int  # 视频ID
    title: str  # 视频标题
    filename: str  # 视频文件名
    description: str  # 视频描述
    file_path: str  # 视频文件存储路径
    cover_path: str | None  # 视频封面图路径，可选
    created_at: datetime  # 创建时间
    upload_time: datetime  # 上传时间
    owner_username: str  # 上传者用户名
    target_type: str | None  # 目标类型（如职位、简历等）
    target_id: int | None  # 目标ID（如职位ID、简历ID等）

    class Config:
        from_attributes = True  # 支持从 ORM 对象读取数据

