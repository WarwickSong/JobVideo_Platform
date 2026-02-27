"""
app/interactions/models.py - 交互行为数据模型

功能说明：
    定义用户与视频交互行为的数据库模型，包括浏览、点赞和收藏等
    使用SQLAlchemy ORM进行数据库映射

数据模型列表：
    - VideoView: 视频浏览记录模型（事件表）
    - VideoLike: 视频点赞模型（状态表）
    - VideoFavorite: 视频收藏模型（状态表）

设计原则：
    - 事件表与状态表分离：浏览记录为事件表，点赞收藏为状态表
    - 使用外键约束确保数据完整性
    - 添加索引优化查询性能
    - 使用唯一约束防止重复数据

@author JobVideo Platform Team
@version 1.0.0
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime, timezone
from app.db import Base


# ==================== 视频浏览记录模型 ====================

class VideoView(Base):
    """
    视频浏览记录模型
    
    表类型：事件表（Event Table）
    
    功能说明：
        记录用户每次浏览视频的行为，用于数据统计和推荐算法
        特点：不做去重，每次浏览都生成新记录
    
    表名：video_views
    
    字段说明：
        - id: 主键，使用BigInteger支持大量数据
        - video_id: 视频ID，外键关联videos表
        - user_id: 用户ID，外键关联users表（可为空，支持未登录用户）
        - created_at: 创建时间，记录浏览发生的时间
    
    索引：
        - id: 主键索引
        - video_id: 外键索引，加速按视频查询
        - user_id: 外键索引，加速按用户查询
        - created_at: 时间索引，加速按时间查询
    
    设计考虑：
        - 使用BigInteger主键：浏览量增长快，需要更大的数值范围
        - nullable=True的user_id：支持未登录用户浏览记录
        - 无唯一约束：每次浏览都生成新记录，不做去重
    
    使用场景：
        - 统计视频浏览量
        - 分析用户浏览行为
        - 推荐算法的数据基础
    """
    
    __tablename__ = "video_views"
    
    # 主键：使用BigInteger支持大量浏览记录
    id: Mapped[BigInteger] = mapped_column(
        BigInteger, 
        primary_key=True, 
        index=True
    )
    
    # 视频ID：外键关联videos表，级联删除
    video_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("videos.id", ondelete="CASCADE"), 
        index=True
    )
    
    # 用户ID：外键关联users表，可为空（支持未登录用户）
    user_id: Mapped[int | None] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=True, 
        index=True
    )
    
    # 创建时间：记录浏览行为发生的时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )


# ==================== 视频点赞模型 ====================

class VideoLike(Base):
    """
    视频点赞模型
    
    表类型：状态表（State Table）
    
    功能说明：
        记录用户对视频的点赞状态
        特点：使用唯一约束确保用户对同一视频只能有一条点赞记录
    
    表名：video_likes
    
    字段说明：
        - id: 主键
        - video_id: 视频ID，外键关联videos表
        - user_id: 用户ID，外键关联users表
        - created_at: 创建时间，记录点赞发生的时间
    
    约束：
        - UNIQUE(video_id, user_id): 确保一个用户对一个视频只能有一条点赞记录
    
    索引：
        - id: 主键索引
        - video_id: 外键索引，加速按视频查询
        - user_id: 外键索引，加速按用户查询
    
    设计考虑：
        - 唯一约束：防止重复点赞
        - 级联删除：视频或用户删除时，相关点赞记录自动删除
        - 记录存在即表示已点赞，记录不存在即表示未点赞
    
    使用场景：
        - 点赞/取消点赞功能
        - 统计视频点赞数
        - 判断用户是否已点赞
    """
    
    __tablename__ = "video_likes"
    
    # 唯一约束：确保一个用户对一个视频只能有一条点赞记录
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_like"),
    )
    
    # 主键
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )
    
    # 视频ID：外键关联videos表，级联删除
    video_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("videos.id", ondelete="CASCADE"), 
        index=True
    )
    
    # 用户ID：外键关联users表，级联删除
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        index=True
    )
    
    # 创建时间：记录点赞行为发生的时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


# ==================== 视频收藏模型 ====================

class VideoFavorite(Base):
    """
    视频收藏模型
    
    表类型：状态表（State Table）
    
    功能说明：
        记录用户对视频的收藏状态
        特点：使用唯一约束确保用户对同一视频只能有一条收藏记录
    
    表名：video_favorites
    
    字段说明：
        - id: 主键
        - video_id: 视频ID，外键关联videos表
        - user_id: 用户ID，外键关联users表
        - created_at: 创建时间，记录收藏发生的时间
    
    约束：
        - UNIQUE(video_id, user_id): 确保一个用户对一个视频只能有一条收藏记录
    
    索引：
        - id: 主键索引
        - video_id: 外键索引，加速按视频查询
        - user_id: 外键索引，加速按用户查询
    
    设计考虑：
        - 唯一约束：防止重复收藏
        - 级联删除：视频或用户删除时，相关收藏记录自动删除
        - 记录存在即表示已收藏，记录不存在即表示未收藏
        - 与VideoLike结构类似，但存储在不同的表中
    
    使用场景：
        - 收藏/取消收藏功能
        - 统计视频收藏数
        - 判断用户是否已收藏
        - 用户收藏列表
    """
    
    __tablename__ = "video_favorites"
    
    # 唯一约束：确保一个用户对一个视频只能有一条收藏记录
    __table_args__ = (
        UniqueConstraint("video_id", "user_id", name="uniq_video_favorite"),
    )
    
    # 主键
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True
    )
    
    # 视频ID：外键关联videos表，级联删除
    video_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("videos.id", ondelete="CASCADE"), 
        index=True
    )
    
    # 用户ID：外键关联users表，级联删除
    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        index=True
    )
    
    # 创建时间：记录收藏行为发生的时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
