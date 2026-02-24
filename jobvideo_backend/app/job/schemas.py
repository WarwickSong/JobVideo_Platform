# app/job/schemas.py
# 职位数据模式
# 功能：定义职位相关的数据验证和响应格式

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 职位基础模式
# 定义职位的基本字段
class JobPostBase(BaseModel):
    title: str  # 职位标题
    description: str  # 职位描述
    salary_min: Optional[float]  # 最低薪资，可选
    salary_max: Optional[float]  # 最高薪资，可选
    location: Optional[str]  # 工作地点，可选

# 职位创建模式
# 用于创建职位时的请求体，继承基础模式
class JobPostCreate(JobPostBase):
    pass

# 职位输出模式
# 用于返回职位信息给客户端
class JobPostOut(JobPostBase):
    id: int  # 职位ID
    status: str  # 职位状态
    created_at: datetime  # 创建时间
    employer_id: int  # 雇主ID

    class Config:
        from_attributes = True  # 支持从 ORM 对象读取数据
