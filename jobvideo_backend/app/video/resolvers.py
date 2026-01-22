# Target Resolver 服务
# app/video/resolvers.py

from sqlalchemy.orm import Session
from typing import Dict, Optional, Any

from app.job.models import JobPost
from app.resume.models import Resume
from app.company.models import Company


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
    解析视频绑定的目标对象
    
    Args:
        target_type: 目标对象类型
        target_id: 目标对象ID
        db: 数据库会话
    
    Returns:
        包含目标对象信息的字典，若不存在返回None
    """
    obj = None
    data = {}
    
    try:
        if target_type == "job":
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
    
    if not obj:
        return None
    
    return {
        "type": target_type,
        "label": TARGET_LABELS.get(target_type, target_type),
        "data": data
    }


def get_target_label(target_type: str) -> str:
    """
    获取目标类型的显示标签
    
    Args:
        target_type: 目标对象类型
    
    Returns:
        目标类型的显示标签
    """
    return TARGET_LABELS.get(target_type, target_type)
