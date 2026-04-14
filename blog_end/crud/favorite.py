from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Article
from models.favorite import Favorite


#检查收藏状态：当前用户是否收藏这一条新闻
async def is_articles_favorite(
        db:AsyncSession,
        user_id: int,
        article_id: int
):
    """检查文章是否被用户收藏"""
    # 查询收藏记录是否存在
    query = select(Favorite).where(Favorite.user_id == user_id,Favorite.article_id == article_id)
    result = await db.execute(query)
    #是否有收藏，返回布尔值
    return result.scalar_one_or_none() is not None

#添加收藏
async def add_articles_favorite(
        db: AsyncSession,
        user_id: int,
        article_id: int
):
    """添加收藏"""
    # 创建新的收藏记录
    new_favorite = Favorite(user_id=user_id, article_id=article_id)
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)
    return new_favorite


async def delete_articles_favorite(
        db: AsyncSession,
        user_id: int,
        article_id: int
):
    """取消收藏"""
    # 删除指定的收藏记录
    query = delete(Favorite).where(Favorite.user_id == user_id, Favorite.article_id == article_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


async def get_favorites_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """获取用户收藏列表"""
    # 统计收藏总数
    query = select(func.count()).where(Favorite.user_id == user_id)
    # query = query.offset((page - 1) * page_size).limit(page_size)
    count_result = await db.execute(query)
    total = count_result.scalar_one()

    #获取收藏列表 + 连表查询 join（） = 收藏时间排序 + 分页
    #select(查寻主体模型类).join(联合查询的模型类，联合查询的条件).where().order_by().offset().limit()
    #别名：Favorite.created_at.label("favorite_time")
    query = (select(
        Article,
        Favorite.created_at.label("favorite_time"),
        Favorite.id.label("favorite_id"))
             .join(Favorite,Favorite.article_id == Article.id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset((page - 1) * page_size)
             .limit(page_size)
             )

    result = await db.execute(query)
    rows = result.all()
    return  rows,total


#清空收藏列表：当前用户 的所有收藏
async def remove_all_favorites(
        db: AsyncSession,
        user_id: int
):
    """删除所有收藏"""
    # 删除用户的所有收藏记录
    query = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0



