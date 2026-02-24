# app/interactions/routes.py
# 交互行为路由
# 功能：定义用户与视频交互的API接口，包括点赞、收藏和浏览接口

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db  # 获取数据库会话的依赖
from app.auth.routes import get_current_user, get_current_user_optional  # 用户认证依赖
from app.auth.models import User  # 用户模型
from app.interactions.services import toggle_video_like, toggle_video_favorite, record_video_view  # 业务逻辑服务
from app.interactions.models import VideoLike, VideoFavorite  # 数据模型


# 创建路由器
# 前缀设置为"/video"，表示所有接口都以"/video"开头
# 标签设置为"video-interactions"，用于API文档分类
router = APIRouter(prefix="/video", tags=["video-interactions"])


@router.post("/{video_id}/like")
def like_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    视频点赞接口：
        用户对视频进行点赞或取消点赞
    
    Args:
        video_id: 视频ID，从路径参数中获取
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        dict: 包含当前点赞状态和总点赞数的字典
    
    Raises:
        HTTPException: 当用户未登录时抛出401错误
    """
    # 调用服务层的toggle_video_like函数处理点赞逻辑
    liked = toggle_video_like(
        db=db,
        video_id=video_id,
        user_id=current_user.id
    )

    # 查询该视频的总点赞数
    like_count = db.query(VideoLike).filter(
        VideoLike.video_id == video_id
    ).count()

    # 返回当前点赞状态和总点赞数
    return {
        "liked": liked,  # 当前用户的点赞状态
        "like_count": like_count  # 视频的总点赞数
    }


@router.post("/{video_id}/favorite")
def favorite_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    视频收藏接口：
        用户对视频进行收藏或取消收藏
    
    Args:
        video_id: 视频ID，从路径参数中获取
        db: 数据库会话
        current_user: 当前登录用户
    
    Returns:
        dict: 包含当前收藏状态和总收藏数的字典
    
    Raises:
        HTTPException: 当用户未登录时抛出401错误
    """
    # 调用服务层的toggle_video_favorite函数处理收藏逻辑
    favorited = toggle_video_favorite(
        db=db,
        video_id=video_id,
        user_id=current_user.id
    )

    # 查询该视频的总收藏数
    favorite_count = db.query(VideoFavorite).filter(
        VideoFavorite.video_id == video_id
    ).count()

    # 返回当前收藏状态和总收藏数
    return {
        "favorited": favorited,  # 当前用户的收藏状态
        "favorite_count": favorite_count  # 视频的总收藏数
    }


@router.post("/{video_id}/view")
def view_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    视频浏览接口：
        记录用户浏览视频的行为
    
    Args:
        video_id: 视频ID，从路径参数中获取
        db: 数据库会话
        current_user: 可选的当前用户（支持未登录）
    
    Returns:
        dict: 包含成功状态的字典
    """
    # 调用服务层的record_video_view函数记录浏览行为
    record_video_view(
        db=db,
        video_id=video_id,
        user_id=current_user.id if current_user else None  # 如果用户登录则传递用户ID，否则为None
    )

    # 返回成功状态
    return {"status": "ok"}
