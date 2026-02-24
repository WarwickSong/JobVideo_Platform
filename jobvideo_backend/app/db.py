# app/db.py
# 数据库配置和连接管理
# 功能：配置数据库连接，提供数据库会话管理

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from app.config import settings

# 数据库连接URL
# 从配置文件中读取数据库连接信息
DATABASE_URL = settings.DATABASE_URL
# 如果是 SQLite，示例：sqlite:///./test.db
# 如果是 PostgreSQL，示例：postgresql://user:password@localhost/dbname

# 创建数据库引擎
# 负责与数据库的底层通信
engine = create_engine(
    DATABASE_URL,
    # 如果是SQLite，需要添加这个参数以允许跨线程访问
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# 创建数据库会话工厂
# 用于创建数据库会话，每个请求使用一个独立的会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建ORM基类
# 所有数据模型都需要继承这个基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖函数：
        用于在FastAPI路由中注入数据库会话
        使用依赖注入可以确保每个请求都有独立的数据库会话
    
    Yields:
        Session: 数据库会话对象
    
    Finally:
        确保会话被正确关闭
    """
    db: Session = SessionLocal()
    try:
        yield db  # 提供数据库会话给路由使用
    finally:
        db.close()  # 确保会话被正确关闭
