# 视频表结构
# app/video/models.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone
from app.db import Base



class Video(Base):
    __tablename__ = "videos"  # 数据库表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # 视频ID，主键
    title: Mapped[str] = mapped_column(String, index=True)  # 视频标题
    filename: Mapped[str] = mapped_column(String, unique=True)  # 视频文件名，唯一
    description: Mapped[str] = mapped_column(String)  # 视频描述
    file_path: Mapped[str] = mapped_column(String)  # 视频文件存储路径
    cover_path: Mapped[str | None] = mapped_column(String, nullable=True)  # 封面图，可为空
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))  # 创建时间
    upload_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))  # 上传时间

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))  # 上传者用户ID

    owner: Mapped["User"] = relationship("User", back_populates="videos")  # 关联用户对象

    # category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))  # 分类ID
    # category: Mapped["Category"] = relationship("Category", back_populates="videos")  # 关联分
