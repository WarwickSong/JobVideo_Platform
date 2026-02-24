# app/interactions/services.py
# 交互行为服务层
# 功能：实现用户与视频交互的核心业务逻辑，包括点赞、收藏和浏览记录

from sqlalchemy.orm import Session
from app.interactions.models import VideoLike, VideoFavorite, VideoView


def toggle_video_like(
    db: Session,
    video_id: int,
    user_id: int
):
    """
    视频点赞/取消点赞功能：
        实现toggle（切换）逻辑：如果已点赞则取消，未点赞则添加
    
    Args:
        db: 数据库会话
        video_id: 视频ID
        user_id: 用户ID
    
    Returns:
        bool: 当前点赞状态（True为已点赞，False为未点赞）
    """
    # 首先查询用户是否已经点赞过该视频
    like = db.query(VideoLike).filter(
        VideoLike.video_id == video_id,
        VideoLike.user_id == user_id
    ).first()

    # 如果已经点赞过，则删除点赞记录（取消点赞）
    if like:
        db.delete(like)  # 删除记录
        db.commit()  # 提交事务
        return False  # 返回未点赞状态
    else:
        # 如果未点赞，则创建新的点赞记录
        new_like = VideoLike(
            video_id=video_id,
            user_id=user_id
        )
        db.add(new_like)  # 添加记录到数据库
        db.commit()  # 提交事务
        return True  # 返回已点赞状态


def toggle_video_favorite(
    db: Session,
    video_id: int,
    user_id: int
):
    """
    视频收藏/取消收藏功能：
        实现toggle（切换）逻辑：如果已收藏则取消，未收藏则添加
    
    Args:
        db: 数据库会话
        video_id: 视频ID
        user_id: 用户ID
    
    Returns:
        bool: 当前收藏状态（True为已收藏，False为未收藏）
    """
    # 首先查询用户是否已经收藏过该视频
    favorite = db.query(VideoFavorite).filter(
        VideoFavorite.video_id == video_id,
        VideoFavorite.user_id == user_id
    ).first()

    # 如果已经收藏过，则删除收藏记录（取消收藏）
    if favorite:
        db.delete(favorite)  # 删除记录
        db.commit()  # 提交事务
        return False  # 返回未收藏状态
    else:
        # 如果未收藏，则创建新的收藏记录
        new_fav = VideoFavorite(
            video_id=video_id,
            user_id=user_id
        )
        db.add(new_fav)  # 添加记录到数据库
        db.commit()  # 提交事务
        return True  # 返回已收藏状态


def record_video_view(
    db: Session,
    video_id: int,
    user_id: int | None
):
    """
    视频浏览记录功能：
        记录用户浏览视频的行为
        特点：不做去重，每次浏览都生成新记录，支持未登录用户
    
    Args:
        db: 数据库会话
        video_id: 视频ID
        user_id: 用户ID（可选，未登录时为None）
    """
    # 创建新的浏览记录
    view = VideoView(
        video_id=video_id,
        user_id=user_id
    )
    db.add(view)  # 添加记录到数据库
    db.commit()  # 提交事务
