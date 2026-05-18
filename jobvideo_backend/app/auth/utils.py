# app/auth/utils.py
# 认证工具函数
# 功能：提供密码加密、验证和JWT令牌生成的工具函数

import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(data: dict):
    """
    创建访问令牌函数：
        生成JWT（JSON Web Token）格式的访问令牌
    
    Args:
        data: 要编码到令牌中的数据（通常包含用户ID）
    
    Returns:
        str: JWT访问令牌
    """
    # 生成 JWT 访问令牌
    # 设置过期时间为配置的分钟数
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})  # 添加过期时间到数据中
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
