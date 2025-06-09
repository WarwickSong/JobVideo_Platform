from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    seeker = "seeker"
    employer = "employer"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        orm_mode = True
