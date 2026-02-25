# app/auth/schemas.py
# 用户数据模式
# 功能：定义用户相关的数据验证和响应格式

from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
import re

# 用户角色枚举
# 定义系统中可用的用户类型
class UserRole(str, Enum):
    seeker = "seeker"  # 求职者
    employer = "employer"  # 雇主

# 用户创建模式
# 用于用户注册时的数据验证
class UserCreate(BaseModel):
    username: str  # 用户名
    phone: str  # 手机号
    password: str  # 密码
    role: UserRole  # 用户角色

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """
        手机号验证函数：
            验证手机号格式是否正确
        
        Args:
            v: 手机号
        
        Returns:
            str: 验证通过的手机号
        
        Raises:
            ValueError: 当手机号格式不正确时抛出异常
        """
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式不正确')
        return v

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
    phone: str  # 手机号
    role: UserRole  # 用户角色

    # 配置：允许从ORM对象创建
    class Config:
        from_attributes = True
