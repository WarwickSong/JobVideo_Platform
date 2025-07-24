from sqlalchemy import Column, Integer, String, Text, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base
from app.auth.models import UserRole

class JobStatus(str, Enum):
    open = "open"
    closed = "closed"

class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    status = Column(Enum("open", "closed", name="jobstatus"), default=JobStatus.open)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    employer_id = Column(Integer, ForeignKey("users.id"))

    employer = relationship("User")
