from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.comment import Comment
from models.users import User


async def create_comment(db: AsyncSession, content: str, article_id: int, user_id: int, parent_id: int = None):
    """创建评论"""
    new_comment = Comment(
        content=content,
        article_id=article_id,
        user_id=user_id,
        parent_id=parent_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def get_article_comments(db: AsyncSession, article_id: int, page: int = 1, size: int = 10):
    """获取文章评论列表（仅顶级评论）"""
    offset = (page - 1) * size

    stmt = (
        select(Comment)
        .where(Comment.article_id == article_id, Comment.parent_id == None)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    result = await db.execute(stmt)
    items = result.scalars().all()

    count_stmt = (
        select(func.count())
        .select_from(Comment)
        .where(Comment.article_id == article_id, Comment.parent_id == None)
    )
    total = (await db.execute(count_stmt)).scalar_one()
    has_more = (offset + len(items)) < total

    return {"items": items, "total": total, "page": page, "size": size, "has_more": has_more}


async def get_comment_replies(db: AsyncSession, parent_id: int):
    """获取评论的回复列表"""
    stmt = (
        select(Comment)
        .where(Comment.parent_id == parent_id)
        .order_by(Comment.created_at.asc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_comment(db: AsyncSession, comment_id: int, user_id: int):
    """删除评论（仅作者可删）"""
    stmt = select(Comment).where(Comment.id == comment_id, Comment.user_id == user_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if comment:
        await db.delete(comment)
        await db.commit()
    return comment
