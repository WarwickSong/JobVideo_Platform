# app/schemas/job.py

from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str

class JobResponse(JobCreate):
    id: int
