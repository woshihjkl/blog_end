from datetime import datetime
from sqlalchemy import Column, UniqueConstraint,Index , Integer,ForeignKey,DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship,DeclarativeBase
from models.article import Article
from models.users import User

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    __tablename__ = "favorite"

    #创建索引    ，，，，UniqueConstraint是唯一约束：当前用户当前新闻只能被收藏一次
    __table_args__ =(
        UniqueConstraint("user_id", "article_id",name="user_articles_unique"),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_articles_idx", "article_id")
    )

    id:Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True,comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False,comment="用户ID")
    article_id: Mapped[int] = mapped_column(Integer,ForeignKey("articles.id"),nullable=False,comment="文章ID")
    created_at: Mapped[datetime] = mapped_column(DATETIME,default=datetime,nullable=False,comment="创建时间")

    def __repr__(self):
        return f"<Favorite(id={self.id},user_id={self.user_id}，article_id={self.article_id},created_at={self.created_at}>"