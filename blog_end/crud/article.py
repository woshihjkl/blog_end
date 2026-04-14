from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.article import Article


async def get_article_by_id(db: AsyncSession, article_id: int):
    """根据ID获取文章"""
    result = await db.execute(select(Article).where(Article.id == article_id))
    return result.scalar_one_or_none()


async def get_articles(db: AsyncSession, page: int = 1, size: int = 10):
    """获取文章列表（分页）"""
    offset = (page - 1) * size
    stmt = select(Article).order_by(Article.created_at.desc()).offset(offset).limit(size)
    result = await db.execute(stmt)
    items = result.scalars().all()

    total = (await db.execute(select(func.count()).select_from(Article))).scalar_one()
    has_more = (offset + len(items)) < total

    return {"items": items, "total": total, "page": page, "size": size, "has_more": has_more}


async def create_article(db: AsyncSession, title: str, content: str, author_id: int):
    """创建新文章"""
    new_article = Article(title=title, content=content, author_id=author_id)
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    return new_article


async def delete_article(db: AsyncSession, article_id: int):
    """删除文章"""
    article = await get_article_by_id(db, article_id)
    if article:
        await db.delete(article)
        await db.commit()
    return article


#搜索文章
async def search_articles(db: AsyncSession, keyword: str, page: int = 1, size: int = 10):
    """搜索文章（支持标题和内容模糊查询）"""
    offset = (page - 1) * size

    stmt = (
        select(Article)
        .where(
            (Article.title.contains(keyword)) |
            (Article.content.contains(keyword))
        )
        .order_by(Article.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    result = await db.execute(stmt)
    items = result.scalars().all()

    count_stmt = (
        select(func.count())
        .select_from(Article)
        .where(
            (Article.title.contains(keyword)) |
            (Article.content.contains(keyword))
        )
    )
    total = (await db.execute(count_stmt)).scalar_one()
    has_more = (offset + len(items)) < total

    return {"items": items, "total": total, "page": page, "size": size, "has_more": has_more}

