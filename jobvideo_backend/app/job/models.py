# app/job/models.py
# 职位数据模型
# 功能：定义职位表结构和职位状态

from sqlalchemy import Column, Integer, String, Text, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base
from app.auth.models import UserRole

# 职位状态枚举
# 定义职位的状态类型
class JobStatus(str, Enum):
    open = "open"  # 招聘中
    closed = "closed"  # 已关闭

# 职位模型
# 定义职位表结构，包含职位的基本信息和状态
class JobPost(Base):
    __tablename__ = "job_posts"  # 数据库表名

    # 职位ID，主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 职位标题
    title = Column(String, index=True)
    
    # 职位描述
    description = Column(Text)
    
    # 最低薪资，可选
    salary_min = Column(Float, nullable=True)
    
    # 最高薪资，可选
    salary_max = Column(Float, nullable=True)
    
    # 工作地点，可选
    location = Column(String, nullable=True)
    
    # 职位状态，默认为招聘中
    status = Column(Enum("open", "closed", name="jobstatus"), default=JobStatus.open)
    
    # 创建时间
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # 雇主ID，外键关联到users表
    employer_id = Column(Integer, ForeignKey("users.id"))

    # 关联的用户对象
    employer = relationship("User")
