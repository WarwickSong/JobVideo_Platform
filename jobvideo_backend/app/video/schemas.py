# Pydantic 请求/响应模型
# app/video/schemas.py

from pydantic import BaseModel
from datetime import datetime

class VideoBase(BaseModel):
    title: str  # 视频标题


class VideoCreate(VideoBase):
    pass  # 创建视频时使用的请求体，继承基础模型


class VideoOut(BaseModel):
    id: int  # 视频ID
    title: str
    filename: str  # 视频文件名
    description: str
    upload_time: datetime  # 上传时间
    file_path: str
    cover_path: str | None
    created_at: datetime
    owner_username: str

    class Config:
        orm_mode = True  # 支持从 ORM 对象读取数据

