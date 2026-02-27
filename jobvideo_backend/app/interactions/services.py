"""
app/interactions/services.py - 交互行为服务层

功能说明：
    实现用户与视频交互的核心业务逻辑，包括点赞、收藏和浏览记录等操作
    作为路由层和数据访问层之间的中间层，封装复杂的业务逻辑

服务函数列表：
    - toggle_video_like: 视频点赞/取消点赞
    - toggle_video_favorite: 视频收藏/取消收藏
    - record_video_view: 记录视频浏览行为

设计原则：
    - 单一职责：每个函数只负责一个具体的业务操作
    - 事务管理：确保数据库操作的原子性
    - 返回值明确：返回操作后的状态，便于上层处理

@author JobVideo Platform Team
@version 1.0.0
"""

from sqlalchemy.orm import Session
from app.interactions.models import VideoLike, VideoFavorite, VideoView


# ==================== 点赞服务 ====================

def toggle_video_like(
    db: Session,
    video_id: int,
    user_id: int
) -> bool:
    """
    视频点赞/取消点赞服务
    
    功能说明：
        实现点赞的toggle（切换）逻辑：
        - 如果用户已点赞，则删除点赞记录（取消点赞）
        - 如果用户未点赞，则创建点赞记录（添加点赞）
    
    Args:
        db (Session): 数据库会话对象
        video_id (int): 视频ID
        user_id (int): 用户ID
    
    Returns:
        bool: 操作后的点赞状态
            - True: 已点赞
            - False: 未点赞
    
    实现逻辑：
        1. 查询用户对该视频的点赞记录
        2. 如果记录存在：删除记录，返回False
        3. 如果记录不存在：创建记录，返回True
        4. 所有数据库操作都立即提交（commit）
    
    Example:
        # 用户首次点赞
        result = toggle_video_like(db, video_id=1, user_id=123)
        # result = True（已点赞）
        
        # 用户再次点击（取消点赞）
        result = toggle_video_like(db, video_id=1, user_id=123)
        # result = False（未点赞）
    
    注意：
        - 数据库操作会立即提交（commit）
        - 依赖数据库的唯一约束防止重复点赞
        - 返回值直接反映当前状态，无需额外查询
    """
    # 查询用户是否已经点赞过该视频
    like = db.query(VideoLike).filter(
        VideoLike.video_id == video_id,
        VideoLike.user_id == user_id
    ).first()

    # 如果已经点赞，则删除记录（取消点赞）
    if like:
        db.delete(like)
        db.commit()
        return False
    else:
        # 如果未点赞，则创建新的点赞记录
        new_like = VideoLike(
            video_id=video_id,
            user_id=user_id
        )
        db.add(new_like)
        db.commit()
        return True


# ==================== 收藏服务 ====================

def toggle_video_favorite(
    db: Session,
    video_id: int,
    user_id: int
) -> bool:
    """
    视频收藏/取消收藏服务
    
    功能说明：
        实现收藏的toggle（切换）逻辑：
        - 如果用户已收藏，则删除收藏记录（取消收藏）
        - 如果用户未收藏，则创建收藏记录（添加收藏）
    
    Args:
        db (Session): 数据库会话对象
        video_id (int): 视频ID
        user_id (int): 用户ID
    
    Returns:
        bool: 操作后的收藏状态
            - True: 已收藏
            - False: 未收藏
    
    实现逻辑：
        1. 查询用户对该视频的收藏记录
        2. 如果记录存在：删除记录，返回False
        3. 如果记录不存在：创建记录，返回True
        4. 所有数据库操作都立即提交（commit）
    
    Example:
        # 用户首次收藏
        result = toggle_video_favorite(db, video_id=1, user_id=123)
        # result = True（已收藏）
        
        # 用户再次点击（取消收藏）
        result = toggle_video_favorite(db, video_id=1, user_id=123)
        # result = False（未收藏）
    
    注意：
        - 数据库操作会立即提交（commit）
        - 依赖数据库的唯一约束防止重复收藏
        - 收藏与点赞是独立的操作，互不影响
        - 返回值直接反映当前状态，无需额外查询
    """
    # 查询用户是否已经收藏过该视频
    favorite = db.query(VideoFavorite).filter(
        VideoFavorite.video_id == video_id,
        VideoFavorite.user_id == user_id
    ).first()

    # 如果已经收藏，则删除记录（取消收藏）
    if favorite:
        db.delete(favorite)
        db.commit()
        return False
    else:
        # 如果未收藏，则创建新的收藏记录
        new_fav = VideoFavorite(
            video_id=video_id,
            user_id=user_id
        )
        db.add(new_fav)
        db.commit()
        return True


# ==================== 浏览记录服务 ====================

def record_video_view(
    db: Session,
    video_id: int,
    user_id: int | None
) -> None:
    """
    视频浏览记录服务
    
    功能说明：
        记录用户浏览视频的行为，用于数据统计和推荐算法
        特点：不做去重，每次浏览都生成新记录
    
    Args:
        db (Session): 数据库会话对象
        video_id (int): 视频ID
        user_id (int | None): 用户ID（可选，未登录时为None）
    
    Returns:
        None: 无返回值
    
    实现逻辑：
        1. 创建新的浏览记录对象
        2. 添加到数据库会话
        3. 提交事务
    
    Example:
        # 已登录用户浏览
        record_video_view(db, video_id=1, user_id=123)
        
        # 未登录用户浏览
        record_video_view(db, video_id=1, user_id=None)
    
    注意：
        - 每次调用都会创建新记录，不做去重
        - 支持未登录用户（user_id为None）
        - 主要用于数据统计、热门视频计算、推荐算法等
        - 数据库操作会立即提交（commit）
    """
    # 创建新的浏览记录
    view = VideoView(
        video_id=video_id,
        user_id=user_id
    )
    
    # 添加记录并提交
    db.add(view)
    db.commit()
