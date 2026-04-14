from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_database
from utils.jwt_handler import decode_access_token
from config.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import crud.users as user_crud

router = APIRouter(prefix="/auth", tags=["认证"])

security = HTTPBearer()

async def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_database)
) -> dict:
    """验证当前用户（依赖注入）"""
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="无效 token")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效 token")

    user = await user_crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
