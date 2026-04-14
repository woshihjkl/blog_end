from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_database
from schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
import crud.article as article_crud

router = APIRouter(prefix="/articles", tags=["文章"])


@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_article(
        article_in: ArticleCreate,
        db: AsyncSession = Depends(get_database)
):
    """创建新文章"""
    # 创建文章（临时固定author_id为1）
    new_article = await article_crud.create_article(
        db=db,
        title=article_in.title,
        content=article_in.content,
        author_id=1
    )
    return new_article


@router.get("/search")
async def search_articles(
        keyword: str = Query(..., min_length=1, description="搜索关键词"),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_database)
):
    """搜索文章（标题或内容包含关键词）"""
    # 执行文章搜索并返回分页结果
    result = await article_crud.search_articles(
        db=db,
        keyword=keyword,
        page=page,
        size=size
    )
    return result


@router.get("/", response_model=ArticleListResponse)
async def list_articles(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_database)
):
    """获取文章列表（分页）"""
    # 查询分页文章数据
    result = await article_crud.get_articles(db=db, page=page, size=size)
    return result


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: AsyncSession = Depends(get_database)):
    """获取文章详情"""
    # 根据ID查询文章
    article = await article_crud.get_article_by_id(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
        article_id: int,
        article_in: ArticleUpdate,
        db: AsyncSession = Depends(get_database)
):
    """更新文章信息"""
    # 查询文章是否存在
    article = await article_crud.get_article_by_id(db=db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 更新文章字段
    if article_in.title is not None:
        article.title = article_in.title
    if article_in.content is not None:
        article.content = article_in.content

    await db.commit()
    await db.refresh(article)
    return article


@router.delete("/{article_id}", status_code=204)
async def delete_article(
        article_id: int,
        db: AsyncSession = Depends(get_database)
):
    """删除文章"""
    # 删除指定文章
    deleted = await article_crud.delete_article(db=db, article_id=article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="文章不存在")
    return None

