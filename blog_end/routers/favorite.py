from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import favorite
from database import get_database
from models import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(article_id: int = Query(..., alias="articleID"),
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_database)
                         ):
    """检查用户是否收藏了商品"""
    # 检查用户是否已收藏该文章
    is_favorited = await favorite.is_articles_favorite(db, user.id, article_id)
    # data是一个对象，构造pydantic类型，构造出对象，返回给前端
    return success_response(message="检查成功", data=FavoriteCheckResponse(isFavorite=is_favorited))


@router.post("/add")
async def add_favorite(data: FavoriteAddRequest,
                       user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_database)
                       ):
    """添加收藏"""
    # 添加文章收藏
    result = await favorite.add_articles_favorite(db, user.id, data.article_id)
    return success_response(message="添加收藏成功", data=result)


@router.delete("/remove")
async def remove_favorite(article_id: int = Query(..., alias="articleID"),
                          user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_database)
                          ):
    """取消收藏"""
    # 取消文章收藏
    result = await favorite.delete_articles_favorite(db, user.id, article_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="取消收藏失败")
    return success_response(message="取消收藏成功")


@router.get("/list")
async def get_favorite_List_(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    """获取用户收藏列表"""
    # 查询用户的收藏列表及总数
    rows, total = await favorite.get_favorites_list(db, user.id, page, page_size)

    # 构造收藏列表数据
    favorite_list = [{
        **articles.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for articles, favorite_time, favorite_id in rows]

    # 判断是否有更多数据
    has_more = total > page * page_size
    data = FavoriteListResponse(
        list=favorite_list,
        total=total,
        hasMore=has_more
    )

    return success_response(message="获取收藏列表成功", data=data)


@router.delete("/clear")
async def clear_favorite(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    """清空用户所有收藏"""
    # 删除用户的所有收藏记录
    count = await favorite.remove_all_favorites(db, user.id)
    return success_response(message=f"清空{count}条收藏记录")
