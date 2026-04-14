from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="评论内容")
    article_id: int = Field(..., description="文章ID")
    parent_id: Optional[int] = Field(None, description="父评论ID（回复时填写）")


class CommentResponse(BaseModel):
    id: int
    content: str
    article_id: int
    user_id: int
    username: Optional[str] = None
    avatar: Optional[str] = None
    parent_id: Optional[int] = None
    created_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    items: List[CommentResponse]
    total: int
    page: int
    size: int
    has_more: bool
