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
                         user : User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_database)
                         ):
    """检查用户是否收藏了商品"""
    is_favorited = await favorite.is_articles_favorite(db, user.id, article_id)
    #data是一个对象，构造pydantic类型，构造出对象，返回给前端
    return success_response(message="检查成功",data=FavoriteCheckResponse(isFavorite=is_favorited))


@router.post("/add")
async def add_favorite(data: FavoriteAddRequest,
                       user : User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_database)
                       ):
    """添加收藏"""
    result = await favorite.add_articles_favorite(db,user.id, data.article_id)
    return success_response(message="添加收藏成功",data=result)

@router.delete("/remove")
async def remove_favorite(article_id: int = Query(..., alias="articleID"),
                       user : User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_database)
                       ):
    """取消收藏"""
    result = await favorite.delete_articles_favorite(db,user.id, article_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="取消收藏失败")
    return success_response(message="取消收藏成功")


@router.get("/list")
async def get_favorite_List_(
        page:int = Query(1,ge = 1),
        page_size : int = Query(10,ge=1,le= 100 , alias="pageSize"),
        user: User = Depends(get_current_user),
        db:AsyncSession = Depends(get_database)
):
     rows,total = await favorite.get_favorites_list(db , user.id , page , page_size)
     favorite_list = [{
         **articles.__dict__,
         "favorite_time": favorite_time,
         "favorite_id": favorite_id
     }for articles,favorite_time,favorite_id in rows]
     has_more = total > page * page_size
     data = FavoriteListResponse(
         list = favorite_list,
         total = total,
         hasMore = has_more
     )

     return success_response(message="获取收藏列表成功",data=data)


@router.delete("/clear")
async def clear_favorite(
        user: User = Depends(get_current_user),
        db:AsyncSession = Depends(get_database)
):

    count = await favorite.remove_all_favorites(db, user.id)
    return success_response(message=f"清空{count}条收藏记录")