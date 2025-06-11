from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from app.db import Base
import enum

class UserRole(str, enum.Enum):
    seeker = "seeker"
    employer = "employer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(SQLAEnum(UserRole), default=UserRole.seeker)
    videos = relationship("Video", back_populates="owner")
    