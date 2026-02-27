"""
app/interactions/schemas.py - 交互行为数据模型

功能说明：
    定义交互行为相关的Pydantic数据模型，用于API请求和响应的数据验证
    确保数据类型正确、字段完整，提供自动的API文档生成

数据模型列表：
    - LikeResponse: 点赞接口响应模型
    - FavoriteResponse: 收藏接口响应模型

设计原则：
    - 使用Pydantic进行数据验证和序列化
    - 字段类型明确，提供详细的字段描述
    - 添加字段验证规则（如ge=0表示不能为负数）
    - 提供示例数据，便于API文档理解

@author JobVideo Platform Team
@version 1.0.0
"""

from pydantic import BaseModel, Field


# ==================== 点赞响应模型 ====================

class LikeResponse(BaseModel):
    """
    点赞接口响应模型
    
    功能说明：
        定义点赞/取消点赞接口的响应数据结构
        确保返回的数据类型正确、字段完整
    
    Attributes:
        liked (bool): 当前用户的点赞状态
            - True: 已点赞
            - False: 未点赞
        like_count (int): 视频的总点赞数
            - 必须 >= 0（使用ge=0验证）
    
    Example:
        {
            "liked": true,
            "like_count": 42
        }
    
    注意：
        - liked字段为boolean类型，表示当前用户状态
        - like_count字段为integer类型，表示总数
        - Field(ge=0)确保like_count不能为负数
    """
    
    liked: bool = Field(
        ...,
        description="当前用户的点赞状态"
    )
    
    like_count: int = Field(
        ...,
        ge=0,
        description="视频的总点赞数，不能为负数"
    )

    class Config:
        """Pydantic配置类"""
        json_schema_extra = {
            "example": {
                "liked": True,
                "like_count": 42
            }
        }


# ==================== 收藏响应模型 ====================

class FavoriteResponse(BaseModel):
    """
    收藏接口响应模型
    
    功能说明：
        定义收藏/取消收藏接口的响应数据结构
        确保返回的数据类型正确、字段完整
    
    Attributes:
        favorited (bool): 当前用户的收藏状态
            - True: 已收藏
            - False: 未收藏
        favorite_count (int): 视频的总收藏数
            - 必须 >= 0（使用ge=0验证）
    
    Example:
        {
            "favorited": true,
            "favorite_count": 15
        }
    
    注意：
        - favorited字段为boolean类型，表示当前用户状态
        - favorite_count字段为integer类型，表示总数
        - Field(ge=0)确保favorite_count不能为负数
        - 收藏与点赞是独立的操作，使用不同的字段名
    """
    
    favorited: bool = Field(
        ...,
        description="当前用户的收藏状态"
    )
    
    favorite_count: int = Field(
        ...,
        ge=0,
        description="视频的总收藏数，不能为负数"
    )

    class Config:
        """Pydantic配置类"""
        json_schema_extra = {
            "example": {
                "favorited": True,
                "favorite_count": 15
            }
        }
