# app/resume/schemas.py
# 简历数据模式
# 功能：定义简历相关的数据验证和响应格式

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 简历基础模式
# 定义简历的基本字段
class ResumeBase(BaseModel):
    title: str  # 职位标题
    skills: str  # 技能列表（JSON或逗号分隔字符串）
    experience_years: int  # 工作经验年限
    major: str  # 专业

# 简历创建模式
# 用于创建简历时的请求体，继承基础模式
class ResumeCreate(ResumeBase):
    pass

# 简历输出模式
# 用于返回简历信息给客户端
class ResumeOut(ResumeBase):
    id: int  # 简历ID

    class Config:
        from_attributes = True  # 支持从 ORM 对象读取数据
