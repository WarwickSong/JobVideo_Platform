# app/resume/models.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
import enum
from app.db import Base

class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)  # 视频标题
    skills: Mapped[str] = mapped_column(String)  # 存 JSON 或逗号分隔字符串
    experience_years: Mapped[int] = mapped_column(Integer)  # 工作经验年限
    major: Mapped[str] = mapped_column(String)  # 专业
