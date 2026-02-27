"""
app/interactions/routes.py - 交互行为路由模块

功能说明：
    定义用户与视频交互的API接口，包括点赞、收藏和浏览记录等操作
    
API接口列表：
    - POST /video/{video_id}/like - 视频点赞/取消点赞
    - POST /video/{video_id}/favorite - 视频收藏/取消收藏
    - POST /video/{video_id}/view - 记录视频浏览行为

设计原则：
    - 遵循RESTful API设计规范
    - 使用依赖注入管理数据库会话和用户认证
    - 统一使用Pydantic模型进行响应数据验证
    - 异常处理返回标准HTTP状态码

@author JobVideo Platform Team
@version 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth.routes import get_current_user, get_current_user_optional
from app.auth.models import User
from app.interactions.services import toggle_video_like, toggle_video_favorite, record_video_view
from app.interactions.models import VideoLike, VideoFavorite
from app.interactions.schemas import LikeResponse, FavoriteResponse


# ==================== 路由器配置 ====================

# 创建路由器实例
# prefix: "/video" - 所有接口都以/video开头
# tags: ["video-interactions"] - API文档分类标签
router = APIRouter(prefix="/video", tags=["video-interactions"])


# ==================== 点赞接口 ====================

@router.post("/{video_id}/like", response_model=LikeResponse)
def like_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    视频点赞/取消点赞接口
    
    功能说明：
        实现视频点赞的toggle逻辑：
        - 如果用户未点赞，则添加点赞记录
        - 如果用户已点赞，则删除点赞记录
    
    Args:
        video_id (int): 视频ID，从URL路径参数获取
        db (Session): 数据库会话，通过依赖注入获取
        current_user (User): 当前登录用户，通过依赖注入获取
    
    Returns:
        LikeResponse: 包含点赞状态和点赞总数的响应对象
            - liked (bool): 当前用户是否已点赞
            - like_count (int): 视频的总点赞数
    
    Raises:
        HTTPException: 
            - 401: 用户未登录
            - 500: 服务器内部错误
    
    Example:
        请求: POST /video/123/like
        响应: {
            "liked": true,
            "like_count": 42
        }
    
    注意：
        - 需要用户登录（通过get_current_user依赖验证）
        - 响应数据经过Pydantic模型验证，确保类型正确
    """
    try:
        # 调用服务层执行toggle操作
        liked = toggle_video_like(
            db=db,
            video_id=video_id,
            user_id=current_user.id
        )

        # 查询该视频的总点赞数
        like_count = db.query(VideoLike).filter(
            VideoLike.video_id == video_id
        ).count()

        # 返回经过Pydantic验证的响应
        return LikeResponse(
            liked=bool(liked),
            like_count=int(like_count)
        )
    except Exception as e:
        # 捕获所有异常，返回500错误
        raise HTTPException(
            status_code=500,
            detail=f"点赞操作失败: {str(e)}"
        )


# ==================== 收藏接口 ====================

@router.post("/{video_id}/favorite", response_model=FavoriteResponse)
def favorite_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    视频收藏/取消收藏接口
    
    功能说明：
        实现视频收藏的toggle逻辑：
        - 如果用户未收藏，则添加收藏记录
        - 如果用户已收藏，则删除收藏记录
    
    Args:
        video_id (int): 视频ID，从URL路径参数获取
        db (Session): 数据库会话，通过依赖注入获取
        current_user (User): 当前登录用户，通过依赖注入获取
    
    Returns:
        FavoriteResponse: 包含收藏状态和收藏总数的响应对象
            - favorited (bool): 当前用户是否已收藏
            - favorite_count (int): 视频的总收藏数
    
    Raises:
        HTTPException:
            - 401: 用户未登录
            - 500: 服务器内部错误
    
    Example:
        请求: POST /video/123/favorite
        响应: {
            "favorited": true,
            "favorite_count": 15
        }
    
    注意：
        - 需要用户登录（通过get_current_user依赖验证）
        - 响应数据经过Pydantic模型验证，确保类型正确
        - 收藏与点赞是独立的操作，互不影响
    """
    try:
        # 调用服务层执行toggle操作
        favorited = toggle_video_favorite(
            db=db,
            video_id=video_id,
            user_id=current_user.id
        )

        # 查询该视频的总收藏数
        favorite_count = db.query(VideoFavorite).filter(
            VideoFavorite.video_id == video_id
        ).count()

        # 返回经过Pydantic验证的响应
        return FavoriteResponse(
            favorited=bool(favorited),
            favorite_count=int(favorite_count)
        )
    except Exception as e:
        # 捕获所有异常，返回500错误
        raise HTTPException(
            status_code=500,
            detail=f"收藏操作失败: {str(e)}"
        )


# ==================== 浏览记录接口 ====================

@router.post("/{video_id}/view")
def view_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    """
    视频浏览记录接口
    
    功能说明：
        记录用户浏览视频的行为，用于数据统计和推荐算法
        支持未登录用户浏览记录（user_id为None）
    
    Args:
        video_id (int): 视频ID，从URL路径参数获取
        db (Session): 数据库会话，通过依赖注入获取
        current_user (User | None): 当前用户（可选），支持未登录访问
    
    Returns:
        dict: 包含操作状态的字典
            - status (str): 操作状态，固定返回"ok"
    
    Example:
        请求: POST /video/123/view
        响应: {
            "status": "ok"
        }
    
    注意：
        - 支持未登录用户（使用get_current_user_optional依赖）
        - 每次浏览都会生成新记录，不做去重
        - 主要用于数据统计和推荐算法
    """
    # 调用服务层记录浏览行为
    record_video_view(
        db=db,
        video_id=video_id,
        user_id=current_user.id if current_user else None
    )

    # 返回成功状态
    return {"status": "ok"}
