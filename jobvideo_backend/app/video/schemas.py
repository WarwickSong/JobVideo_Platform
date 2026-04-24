# app/video/schemas.py
# 视频数据模式
# 功能：定义视频相关的数据验证和响应格式

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from app.video.models import TargetType


# 职位摘要模式
# 用于在视频feed中显示职位的基本信息
class JobSummary(BaseModel):
    id: int  # 职位ID
    title: str  # 职位标题
    location: str  # 工作地点
    salary_min: int  # 最低薪资
    salary_max: int  # 最高薪资


# 简历摘要模式
# 用于在视频feed中显示简历的基本信息
class ResumeSummary(BaseModel):
    id: int  # 简历ID
    title: str  # 职位标题
    experience_years: int  # 工作年限
    skills: list[str]  # 技能列表
    major: str  # 专业


# 公司介绍摘要模式
# 用于在视频feed中显示公司的基本信息
class CompanyIntroSummary(BaseModel):
    id: int  # 公司ID
    name: str  # 公司名称
    industry: str  # 行业
    location: str  # 所在地


# 带目标的视频模式
# 用于视频feed接口，包含视频信息和绑定的目标对象摘要
class VideoWithTarget(BaseModel):
    id: int  # 视频ID
    title: str  # 视频标题
    filename: str  # 视频文件名
    description: str  # 视频描述
    file_path: str  # 视频文件路径
    cover_path: str | None  # 视频封面路径
    created_at: datetime  # 创建时间
    upload_time: datetime  # 上传时间
    owner_username: str  # 上传者用户名
    owner_role: str | None  # 上传者角色
    target_type: TargetType | None  # 目标类型
    target_id: int | None  # 目标ID
    target_summary: dict | None  # 目标对象摘要，由后端构造
    like_count: int  # 点赞数
    favorite_count: int  # 收藏数
    is_liked_by_me: bool  # 当前用户是否点赞
    is_favorited_by_me: bool  # 当前用户是否收藏

    class Config:
        from_attributes = True


# 视频基础模式
# 定义视频的基本字段
class VideoBase(BaseModel):
    title: str  # 视频标题


# 视频创建模式
# 用于创建视频时的请求体
class VideoCreate(VideoBase):
    title: str  # 视频标题
    description: str  # 视频描述
    target_type: TargetType | None = None  # 目标类型
    target_id: int | None = None  # 目标ID


# 视频输出模式
# 用于返回视频信息给客户端
class VideoOut(BaseModel):
    id: int  # 视频ID
    title: str  # 视频标题
    filename: str  # 视频文件名
    description: str  # 视频描述
    file_path: str  # 视频文件路径
    cover_path: str | None  # 视频封面路径
    created_at: datetime  # 创建时间
    upload_time: datetime  # 上传时间
    owner_username: str  # 上传者用户名
    target_type: str | None  # 目标类型
    target_id: int | None  # 目标ID

    class Config:
        from_attributes = True  # 支持从 ORM 对象读取数据


# 视频目标模式
# 用于表示视频绑定的目标对象
class VideoTarget(BaseModel):
    type: str  # 目标类型
    label: str  # 目标类型的显示标签
    data: dict  # 目标对象的详细数据


# 视频详情模式
# 用于返回视频的完整信息，包括绑定的目标对象
class VideoDetail(BaseModel):
    id: int  # 视频ID
    title: str  # 视频标题
    description: str  # 视频描述
    file_path: str  # 视频文件路径
    filename: str  # 视频文件名
    cover_path: str | None  # 视频封面路径
    created_at: datetime  # 创建时间
    upload_time: datetime  # 上传时间
    owner_username: str  # 上传者用户名
    target: VideoTarget | None  # 绑定的目标对象
    like_count: int  # 点赞数
    favorite_count: int  # 收藏数
    is_liked_by_me: bool  # 当前用户是否点赞
    is_favorited_by_me: bool  # 当前用户是否收藏
