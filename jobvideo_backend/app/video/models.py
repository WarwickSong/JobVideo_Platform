# 视频表结构
# app/video/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base

class Video(Base):
    __tablename__ = "videos"  # 数据库表名

    id = Column(Integer, primary_key=True, index=True)  # 视频ID，主键
    title = Column(String, index=True)  # 视频标题
    filename = Column(String, unique=True)  # 视频文件名，唯一
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # 上传时间，默认为当前时间（UTC，带时区）
    owner_id = Column(Integer, ForeignKey("users.id"))  # 上传者用户ID，外键关联users表

    owner = relationship("User", back_populates="videos")  # 关联用户对象，实现反向引用

