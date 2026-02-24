# app/video/resolvers.py
# 目标对象解析服务
# 功能：解析视频绑定的目标对象（职位、简历、公司介绍），提供统一的数据格式

from sqlalchemy.orm import Session
from typing import Dict, Optional, Any

from app.job.models import JobPost
from app.resume.models import Resume
from app.company.models import Company

# 目标类型标签映射
# 用于将目标类型转换为中文显示标签
TARGET_LABELS = {
    "job": "职位",
    "resume": "简历",
    "company_intro": "公司介绍"
}


def resolve_target(
    target_type: str,
    target_id: int,
    db: Session
) -> Optional[Dict[str, Any]]:
    """
    解析目标对象函数：
        根据目标类型和ID，从数据库中查询并返回目标对象的详细信息
    
    Args:
        target_type: 目标对象类型（job、resume、company_intro）
        target_id: 目标对象ID
        db: 数据库会话
    
    Returns:
        Optional[Dict[str, Any]]: 包含目标对象信息的字典，若不存在返回None
    """
    obj = None
    data = {}
    
    try:
        # 根据目标类型查询不同的表
        if target_type == "job":
            # 查询职位信息
            obj = db.query(JobPost).filter(JobPost.id == target_id).first()
            if obj:
                data = {
                    "id": obj.id,
                    "title": obj.title,
                    "description": obj.description,
                    "location": obj.location,
                    "salary_min": obj.salary_min,
                    "salary_max": obj.salary_max,
                    "experience_years": obj.experience_years,
                    "education": obj.education,
                    "skills": obj.skills.split(",") if obj.skills else [],
                    "posted_at": obj.posted_at,
                    "status": obj.status
                }
        
        elif target_type == "resume":
            # 查询简历信息
            obj = db.query(Resume).filter(Resume.id == target_id).first()
            if obj:
                data = {
                    "id": obj.id,
                    "title": obj.title,
                    "description": obj.description,
                    "experience_years": obj.experience_years,
                    "education": obj.education,
                    "major": obj.major,
                    "skills": obj.skills.split(",") if obj.skills else [],
                    "self_introduction": obj.self_introduction,
                    "created_at": obj.created_at
                }
        
        elif target_type == "company_intro":
            # 查询公司介绍信息
            obj = db.query(Company).filter(Company.id == target_id).first()
            if obj:
                data = {
                    "id": obj.id,
                    "name": obj.name,
                    "industry": obj.industry,
                    "location": obj.location,
                    "size": obj.size,
                    "description": obj.description,
                    "logo": obj.logo,
                    "established_at": obj.established_at
                }
    except Exception:
        # 按照要求，不抛异常，返回None
        return None
    
    # 如果对象不存在，返回None
    if not obj:
        return None
    
    # 返回统一格式的目标对象信息
    return {
        "type": target_type,
        "label": TARGET_LABELS.get(target_type, target_type),
        "data": data
    }


def get_target_label(target_type: str) -> str:
    """
    获取目标类型标签函数：
        根据目标类型返回对应的中文显示标签
    
    Args:
        target_type: 目标对象类型
    
    Returns:
        str: 目标类型的中文显示标签
    """
    return TARGET_LABELS.get(target_type, target_type)
