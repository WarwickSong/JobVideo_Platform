from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobPostBase(BaseModel):
    title: str
    description: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    location: Optional[str]

class JobPostCreate(JobPostBase):
    pass

class JobPostOut(JobPostBase):
    id: int
    status: str
    created_at: datetime
    employer_id: int

    class Config:
        from_attributes = True
