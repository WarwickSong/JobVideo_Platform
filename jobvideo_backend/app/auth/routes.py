# app/auth/routes.py

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db
from app.config import settings
from app.auth import schemas, models, utils

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 注册接口
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(400, detail="用户名已存在")
    # 创建新用户
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=utils.hash_password(user.password),
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 登录接口
@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    # 查询用户并校验密码
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not utils.verify_password(data.password, user.password_hash):
        raise HTTPException(401, detail="用户名或密码错误")
    # 生成 JWT token
    token = utils.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(401, detail="Token 无效")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(401, detail="Token 无效")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="用户不存在")
    return user

# 获取当前用户信息接口
@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

# 列出所有用户接口
@router.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    # 查询所有用户
    users = db.query(models.User).all()
    return users

