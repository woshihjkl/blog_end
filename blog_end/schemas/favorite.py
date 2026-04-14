from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import ArticlesBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


class FavoriteAddRequest(BaseModel):
    article_id: int = Field(..., alias="articleID")

#两个类：文章模型类 + 收藏模型类
class FavoriteArticlesItemResponse(ArticlesBase):
    favorite_id: int = Field(..., alias="favoriteId")
    favorite_time: datetime = Field(..., alias="favoriteTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

#收藏列表接口相应的模型类
class FavoriteListResponse(BaseModel):
    list : list[FavoriteArticlesItemResponse]
    total : int
    has_more : bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
