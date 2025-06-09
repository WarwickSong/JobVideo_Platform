from sqlalchemy import Column, Integer, String, Enum
from app.db import Base
import enum

class UserRole(str, enum.Enum):
    seeker = "seeker"
    employer = "employer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.seeker)
