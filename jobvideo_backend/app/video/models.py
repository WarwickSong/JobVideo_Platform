# app/video/models.py
# 视频数据模型
# 功能：定义视频表结构和视频可以绑定的目标类型

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
import enum
from app.db import Base


# 目标类型枚举
# 定义视频可以绑定的业务对象类型
class TargetType(str, enum.Enum):
    job = "job"  # 职位
    resume = "resume"  # 简历
    company_intro = "company_intro"  # 公司介绍


# 视频模型
# 定义视频表结构，包含视频的基本信息和关联信息
class Video(Base):
    __tablename__ = "videos"  # 数据库表名

    # 视频ID，主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 视频标题
    title: Mapped[str] = mapped_column(String, index=True)
    
    # 视频文件名，唯一
    filename: Mapped[str] = mapped_column(String, unique=True)
    
    # 视频描述
    description: Mapped[str] = mapped_column(String)
    
    # 视频文件存储路径
    file_path: Mapped[str] = mapped_column(String)
    
    # 封面图路径，可为空
    cover_path: Mapped[str | None] = mapped_column(String, nullable=True)
    
    # 创建时间
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # 上传时间
    upload_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 上传者用户ID，外键关联到users表
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    # 关联的用户对象
    owner: Mapped["User"] = relationship("User", back_populates="videos")

    # 泛型绑定字段
    # 允许视频绑定到不同的业务对象（职位、简历、公司介绍等）
    target_type: Mapped[TargetType | None] = mapped_column(SqlEnum(TargetType), nullable=True)
    target_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 其他注释的关联关系（预留）
    # category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))  # 分类ID
    # category: Mapped["Category"] = relationship("Category", back_populates="videos")  # 关联分类
