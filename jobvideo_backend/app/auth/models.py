# app/auth/models.py
# 用户数据模型
# 功能：定义用户表结构和用户角色

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from app.db import Base  # 导入基础模型
import enum

# 用户角色枚举
# 定义系统中可用的用户类型
class UserRole(str, enum.Enum):
    seeker = "seeker"  # 求职者
    employer = "employer"  # 雇主


# 用户模型
# 定义用户表结构，包含用户的基本信息和角色
class User(Base):
    __tablename__ = "users"  # 数据库表名

    # 用户ID，主键
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # 用户名，唯一且可索引
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # 邮箱，唯一且可索引
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # 密码哈希值（加密存储）
    password_hash: Mapped[str] = mapped_column(String)
    
    # 用户角色，默认为求职者
    role: Mapped[UserRole] = mapped_column(SQLAEnum(UserRole), default=UserRole.seeker)

    # 与视频模型的关系，一个用户可以上传多个视频
    videos: Mapped[list["Video"]] = relationship("Video", back_populates="owner")
