# app/auth/deps.py
# 认证依赖项
# 功能：提供基于角色的访问控制依赖

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.routes import get_current_user
from app.auth.models import UserRole, User


def role_required(required_role: UserRole):
    """
    角色权限检查依赖：
        用于限制某些接口只能由特定角色的用户访问
    
    Args:
        required_role: 要求的用户角色
    
    Returns:
        wrapper: 依赖函数，用于在路由中使用
    
    Raises:
        HTTPException: 当用户角色不符合要求时抛出403错误
    """
    # 内层函数：实际的依赖项逻辑
    def wrapper(current_user: User = Depends(get_current_user)):
        # 检查当前用户的角色是否符合要求
        if str(current_user.role) != str(required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,  # 403 Forbidden
                detail=f"当前用户没有权限，必须是 {required_role}",
            )
        return current_user
    return wrapper
