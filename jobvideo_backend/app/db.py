# app/db.py

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import settings


DATABASE_URL = settings.DATABASE_URL
# 如果是 SQLite，示例：sqlite:///./test.db
# 如果是 PostgreSQL，示例：postgresql://user:password@localhost/dbname

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
