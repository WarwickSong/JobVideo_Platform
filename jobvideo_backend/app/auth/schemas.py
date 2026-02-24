# app/auth/schemas.py
# 用户数据模式
# 功能：定义用户相关的数据验证和响应格式

from pydantic import BaseModel, EmailStr
from enum import Enum

# 用户角色枚举
# 定义系统中可用的用户类型
class UserRole(str, Enum):
    seeker = "seeker"  # 求职者
    employer = "employer"  # 雇主

# 用户创建模式
# 用于用户注册时的数据验证
class UserCreate(BaseModel):
    username: str  # 用户名
    email: EmailStr  # 邮箱（自动验证格式）
    password: str  # 密码
    role: UserRole  # 用户角色

# 用户登录模式
# 用于用户登录时的数据验证
class UserLogin(BaseModel):
    username: str  # 用户名
    password: str  # 密码

# 用户输出模式
# 用于返回用户信息给客户端
class UserOut(BaseModel):
    id: int  # 用户ID
    username: str  # 用户名
    email: EmailStr  # 邮箱
    role: UserRole  # 用户角色

    # 配置：允许从ORM对象创建
    class Config:
        from_attributes = True
