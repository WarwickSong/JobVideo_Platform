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
    title: str  # 视频标题
    filename: str  # 视频文件名
    description: str  # 视频描述
    file_path: str  # 视频文件存储路径
    cover_path: str | None  # 视频封面图路径，可选
    created_at: datetime  # 创建时间
    upload_time: datetime  # 上传时间
    owner_username: str  # 上传者用户名

    class Config:
        from_attributes = True  # 支持从 ORM 对象读取数据

