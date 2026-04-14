from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import ArticlesBase


class FavoriteCheckResponse(BaseModel):
    """收藏状态检查响应模型"""
    is_favorite: bool = Field(..., alias="isFavorite")


class FavoriteAddRequest(BaseModel):
    """添加收藏请求模型"""
    article_id: int = Field(..., alias="articleID")

#两个类：文章模型类 + 收藏模型类
class FavoriteArticlesItemResponse(ArticlesBase):
    """收藏文章项响应模型"""
    favorite_id: int = Field(..., alias="favoriteId")
    favorite_time: datetime = Field(..., alias="favoriteTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

#收藏列表接口相应的模型类
class FavoriteListResponse(BaseModel):
    """收藏列表响应模型"""
    list : list[FavoriteArticlesItemResponse]
    total : int
    has_more : bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

