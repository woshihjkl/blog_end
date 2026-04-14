from typing import Optional

from sqlalchemy import String, func, Index, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    # 索引
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    create_time: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=True, index=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None, comment="用户简介")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None, comment="用户头像")
    articles: Mapped[list["Article"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")


class UserToken(Base):
    __tablename__ = "user_tokens"


    __table_args__ = (
        Index('token_UNIQUE', 'token', unique=True),
        Index('fk_user_token_user_idx', 'user_id', unique=True),
    )


    id: Mapped[int] = mapped_column(primary_key=True, index=True,autoincrement=True,comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False,comment="用户ID")
    token: Mapped[str] =mapped_column(String(255),unique=True,nullable=False,comment="令牌值")
    create_time: Mapped[datetime] = mapped_column(DateTime,default=datetime.now(), nullable=False,comment="令牌创建时间")
    expire_time: Mapped[datetime] = mapped_column(DateTime,nullable=False,comment="令牌过期时间")


    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token})>"