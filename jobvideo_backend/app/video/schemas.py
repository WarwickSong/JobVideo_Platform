# Pydantic 请求/响应模型
# app/video/schemas.py

from pydantic import BaseModel
from datetime import datetime

class VideoBase(BaseModel):
    title: str  # 视频标题

class VideoCreate(VideoBase):
    pass  # 创建视频时使用的请求体，继承基础模型

class VideoOut(VideoBase):
    id: int  # 视频ID
    filename: str  # 视频文件名
    upload_time: datetime  # 上传时间

    class Config:
        orm_mode = True  # 支持从 ORM 对象读取数据

