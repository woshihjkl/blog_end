from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="评论内容")
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False, comment="文章ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="用户ID")
    parent_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True, default=None, comment="父评论ID（回复）")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), comment="更新时间")

    article: Mapped["Article"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")
    parent: Mapped["Comment"] = relationship(remote_side=[id], back_populates="replies")
    replies: Mapped[list["Comment"]] = relationship(back_populates="parent")
