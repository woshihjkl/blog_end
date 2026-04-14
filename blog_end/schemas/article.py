from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class ArticleCreate(BaseModel):
    """创建文章请求模型"""
    title: str
    content: str


class ArticleUpdate(BaseModel):
    """更新文章请求模型"""
    title: str | None = None
    content: str | None = None


class ArticleResponse(BaseModel):
    """文章响应模型"""
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleListResponse(BaseModel):
    """文章列表响应模型"""
    items: List[ArticleResponse]
    total: int
    page: int
    size: int
    has_more: bool

    model_config = ConfigDict(from_attributes=True)

