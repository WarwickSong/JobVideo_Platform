# app/auth/utils.py
# 认证工具函数
# 功能：提供密码加密、验证和JWT令牌生成的工具函数

from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    """
    密码加密函数：
        使用bcrypt算法对密码进行加密，提高安全性
    
    Args:
        password: 明文密码
    
    Returns:
        str: 加密后的密码哈希值
    """
    return bcrypt.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    密码验证函数：
        验证明文密码与加密后的哈希值是否匹配
    
    Args:
        password: 明文密码
        hashed: 加密后的密码哈希值
    
    Returns:
        bool: 密码是否匹配
    """
    return bcrypt.verify(password, hashed)


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
