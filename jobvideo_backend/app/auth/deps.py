from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.routes import get_current_user
from app.auth.models import UserRole, User

def role_required(required_role: UserRole):
    def wrapper(current_user: User = Depends(get_current_user)):
        if str(current_user.role) != str(required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"当前用户没有权限，必须是 {required_role}",
            )
        return current_user
    return wrapper
