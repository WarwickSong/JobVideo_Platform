# app/company/models.py
# 公司数据模型
# 功能：定义公司表结构

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
import enum
from app.db import Base

# 公司模型
# 定义公司表结构，包含公司的基本信息
class Company(Base):
    __tablename__ = "companies"  # 数据库表名
    
    # 公司ID，主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 公司名称
    name: Mapped[str] = mapped_column(String)
    
    # 所属行业
    industry: Mapped[str] = mapped_column(String)
    
    # 公司地点
    location: Mapped[str] = mapped_column(String)
