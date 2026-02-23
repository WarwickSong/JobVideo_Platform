from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime, timezone
from app.db import Base


class VideoView(Base):
    __tablename__ = "video_views"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, index=True)
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )


class VideoLike(Base):
    __tablename__ = "video_likes"
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_like"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


class VideoFavorite(Base):
    __tablename__ = "video_favorites"
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_favorite"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
