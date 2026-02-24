# app/resume/models.py
# 简历数据模型
# 功能：定义简历表结构

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
import enum
from app.db import Base

# 简历模型
# 定义简历表结构，包含求职者的基本信息
class Resume(Base):
    __tablename__ = "resumes"  # 数据库表名
    
    # 简历ID，主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 职位标题
    title: Mapped[str] = mapped_column(String, index=True)
    
    # 技能列表，存储为JSON或逗号分隔字符串
    skills: Mapped[str] = mapped_column(String)
    
    # 工作经验年限
    experience_years: Mapped[int] = mapped_column(Integer)
    
    # 专业
    major: Mapped[str] = mapped_column(String)
