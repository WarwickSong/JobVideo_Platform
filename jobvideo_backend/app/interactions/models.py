# app/interactions/models.py
# 交互行为数据模型
# 功能：定义用户与视频交互的行为数据结构，包括浏览、点赞和收藏

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime, timezone
from app.db import Base


# 视频浏览记录模型
# 这是一个事件表，记录用户每次浏览视频的行为
# 特点：支持未登录用户，不做去重，每次浏览都生成新记录
class VideoView(Base):
    __tablename__ = "video_views"  # 数据库表名

    # 主键，使用BigInteger类型以支持大量数据
    # BigInteger可以存储更大的数字，适合浏览量这种增长很快的场景
    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, index=True)
    
    # 视频ID，外键关联到videos表
    # ondelete="CASCADE"表示当视频被删除时，相关的浏览记录也会被自动删除
    # index=True添加索引，加快查询速度
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    
    # 用户ID，外键关联到users表
    # nullable=True表示可以为空，支持未登录用户浏览视频
    # index=True添加索引，加快查询速度
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # 创建时间
    # 记录浏览行为发生的时间
    # index=True添加索引，便于按时间查询和排序
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),  # 默认值为当前时间
        index=True
    )


# 视频点赞模型
# 这是一个状态表，记录用户对视频的点赞状态
# 特点：使用唯一约束确保用户对同一视频只能有一条点赞记录
class VideoLike(Base):
    __tablename__ = "video_likes"  # 数据库表名
    
    # 添加唯一约束，确保一个用户对一个视频只能有一条点赞记录
    # 这样可以防止重复点赞
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_like"),
    )

    # 主键，使用Integer类型即可
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 视频ID，外键关联到videos表
    # ondelete="CASCADE"表示当视频被删除时，相关的点赞记录也会被自动删除
    # index=True添加索引，加快查询速度
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    
    # 用户ID，外键关联到users表
    # ondelete="CASCADE"表示当用户被删除时，相关的点赞记录也会被自动删除
    # index=True添加索引，加快查询速度
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    # 创建时间
    # 记录点赞行为发生的时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)  # 默认值为当前时间
    )


# 视频收藏模型
# 这是一个状态表，记录用户对视频的收藏状态
# 特点：与VideoLike结构类似，使用唯一约束确保用户对同一视频只能有一条收藏记录
class VideoFavorite(Base):
    __tablename__ = "video_favorites"  # 数据库表名
    
    # 添加唯一约束，确保一个用户对一个视频只能有一条收藏记录
    # 这样可以防止重复收藏
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_favorite"),
    )

    # 主键，使用Integer类型即可
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # 视频ID，外键关联到videos表
    # ondelete="CASCADE"表示当视频被删除时，相关的收藏记录也会被自动删除
    # index=True添加索引，加快查询速度
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), index=True)
    
    # 用户ID，外键关联到users表
    # ondelete="CASCADE"表示当用户被删除时，相关的收藏记录也会被自动删除
    # index=True添加索引，加快查询速度
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    # 创建时间
    # 记录收藏行为发生的时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)  # 默认值为当前时间
    )
