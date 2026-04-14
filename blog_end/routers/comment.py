from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import comment as comment_crud
from database import get_database
from models import User, Comment
from schemas.comment import CommentCreate, CommentResponse, CommentListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/comments", tags=["评论"])


@router.post("/", status_code=201)
async def create_comment(
        data: CommentCreate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    """发表评论或回复"""
    new_comment = await comment_crud.create_comment(
        db=db,
        content=data.content,
        article_id=data.article_id,
        user_id=user.id,
        parent_id=data.parent_id
    )

    response_data = CommentResponse.model_validate(new_comment)
    return success_response(message="评论成功", data=response_data)


@router.get("/article/{article_id}")
async def get_article_comments(
        article_id: int,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_database)
):
    """获取文章评论列表"""
    result = await comment_crud.get_article_comments(
        db=db,
        article_id=article_id,
        page=page,
        size=size
    )

    comments_with_replies = []
    for comment in result["items"]:
        comment_dict = CommentResponse.model_validate(comment).model_dump()
        replies = await comment_crud.get_comment_replies(db, comment.id)
        comment_dict["replies"] = [CommentResponse.model_validate(r).model_dump() for r in replies]
        comments_with_replies.append(comment_dict)

    response_data = CommentListResponse(
        items=comments_with_replies,
        total=result["total"],
        page=result["page"],
        size=result["size"],
        has_more=result["has_more"]
    )

    return success_response(message="获取评论列表成功", data=response_data)


@router.delete("/{comment_id}")
async def delete_comment(
        comment_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    """删除评论"""
    deleted = await comment_crud.delete_comment(
        db=db,
        comment_id=comment_id,
        user_id=user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在或无权限删除"
        )

    return success_response(message="删除评论成功")
