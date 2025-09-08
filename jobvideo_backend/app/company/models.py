# app/company/models.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
import enum
from app.db import Base

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
