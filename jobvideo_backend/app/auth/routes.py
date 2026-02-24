# app/auth/routes.py
# 认证模块路由
# 功能：实现用户注册、登录和认证相关的API接口

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db  # 获取数据库会话的依赖
from app.config import settings  # 应用配置（包含密钥等）
from app.auth import schemas, models, utils  # 认证相关模块

# 创建路由器
# 前缀设置为"/auth"，表示所有接口都以"/auth"开头
# 标签设置为"Auth"，用于API文档分类
router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2密码认证方案
# tokenUrl指定登录接口的路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口：
        创建新用户账号
    
    Args:
        user: 用户注册信息（用户名、邮箱、密码、角色）
        db: 数据库会话
    
    Returns:
        UserOut: 新创建的用户信息
    
    Raises:
        HTTPException: 当用户名已存在时抛出400错误
    """
    # 检查用户名是否已存在
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(400, detail="用户名已存在")
    
    # 创建新用户
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=utils.hash_password(user.password),  # 密码加密存储
        role=user.role,  # 用户角色
    )
    
    # 保存到数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 刷新获取最新数据
    
    return new_user


@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口：
        用户登录并获取访问令牌
    
    Args:
        data: 登录信息（用户名、密码）
        db: 数据库会话
    
    Returns:
        dict: 包含访问令牌和令牌类型的字典
    
    Raises:
        HTTPException: 当用户名或密码错误时抛出401错误
    """
    # 查询用户并校验密码
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not utils.verify_password(data.password, user.password_hash):
        raise HTTPException(401, detail="用户名或密码错误")
    
    # 生成 JWT token
    # JWT (JSON Web Token) 是一种安全的令牌格式，用于身份验证
    token = utils.create_access_token({"sub": str(user.id)})
    
    # 返回令牌和令牌类型
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    获取当前用户：
        从请求中提取令牌，验证并返回当前登录用户
        这是一个依赖函数，被其他需要认证的接口使用
    
    Args:
        token: 从请求头中提取的JWT令牌
        db: 数据库会话
    
    Returns:
        User: 当前登录的用户对象
    
    Raises:
        HTTPException: 当令牌无效或用户不存在时抛出401或404错误
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(401, detail="Token 无效")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(401, detail="Token 无效")
    
    # 根据用户ID查询用户
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="用户不存在")
    
    return user


def get_current_user_optional(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    获取可选的当前用户：
        从请求中提取令牌，验证并返回当前登录用户，如果令牌无效则返回None
        这是一个依赖函数，被允许未登录访问的接口使用
    
    Args:
        token: 从请求头中提取的JWT令牌
        db: 数据库会话
    
    Returns:
        User | None: 当前登录的用户对象或None（未登录）
    """
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            return None
        user_id = int(sub)
    except (JWTError, ValueError):
        return None
    
    # 根据用户ID查询用户
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """
    获取当前用户信息接口：
        返回当前登录用户的详细信息
    
    Args:
        current_user: 当前登录的用户对象
    
    Returns:
        UserOut: 当前用户的详细信息
    """
    return current_user


@router.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    """
    列出所有用户接口：
        返回系统中所有用户的列表
    
    Args:
        db: 数据库会话
    
    Returns:
        list[UserOut]: 所有用户的列表
    """
    # 查询所有用户
    users = db.query(models.User).all()
    return users
