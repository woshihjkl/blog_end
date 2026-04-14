import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.users import User, UserToken
from schemas import UserCreate
from schemas.users import UserUpdateRequest
from utils import security

async def get_user_by_username(db: AsyncSession, username: str):
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data:UserCreate):
    #密码加密
    hashed_password = security.get_hash_password(user_data.password)
    new_user = User(username=user_data.username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def create_token(db: AsyncSession, user_id: int):
    token: str = str(uuid.uuid4())
    expire_time = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expire_time = expire_time
    else:
        user_token = UserToken(user_id=user_id, token=token, expire_time=expire_time)
    db.add(user_token)
    await db.commit()

    return token

#验证用户凭据
async def authenticate_user(db: AsyncSession, username: str, password: str):

    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


#根据Token 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(User).join(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expire_time < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):

    query = await db.execute(
        update(User).where(User.username == username).values(
            user_data.model_dump(exclude_unset=True,
                                 exclude_none=True
            )
        )
    )
    await db.commit()

    #检查更新
    if query.rowcount == 0:  #没有命中数据
        raise HTTPException(status_code=404, detail="用户不存在")

    #获取更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user


#修改密码
async def change_password(
        db: AsyncSession,
        user: str,
        old_password: str,
        new_password: str
):
    if not security.verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="旧密码错误")
    user.password = security.get_hash_password(new_password)
    #更新：由SQLALchemy真正接管User对象。确保commit
    #规避session过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True