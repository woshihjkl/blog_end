from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from database import get_database
from models import User
from schemas.users import UserCreate, UserResponse, UserAuthResponse, UserInfoResponse, UserUpdateRequest, \
    UserChangePasswordRequest
from utils.auth import get_current_user
from utils.jwt_handler import create_access_token
import crud.users as user_crud
from utils.response import success_response
from utils.security import verify_password

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post("/register", status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_database)):
    """用户注册"""
    exist_user = await user_crud.get_user_by_username(db=db, username=user_in.username)
    if exist_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = await user_crud.create_user(db, user_data=user_in)

    token = await users.create_token(db, new_user.id)

    # return {
    #     "code": 201,
    #     "msg": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": new_user.id,
    #             "username": new_user.username,
    #             "bio": new_user.bio,
    #             "avatar": new_user.avatar,
    #         }
    #     }
    # }

    response_data = UserAuthResponse(token = token, user_info = UserInfoResponse.model_validate(new_user))
    return success_response(message="注册成功", data=response_data)



@router.post("/login")
async def login(user_data:UserCreate, db: AsyncSession = Depends(get_database)):
    """验证用户凭据"""
    user = await user_crud.authenticate_user(db=db, username=user_data.username, password=user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token = token, user_info = UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)

@router.get("/{username}", response_model=UserResponse)
async def get_user(username: str, db: AsyncSession = Depends(get_database)):
    """获取用户信息"""
    user = await user_crud.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return user

#查Token 查用户
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

#修改用户信息 1，验证token   2，更新数据（put，请求体，定义pydantic）  3，响应
#参数：用户输入 + 验证token + db
@router.put("/update")
async def update_user_info(
        user_data : UserUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    user = await user_crud.update_user(db, user.username, user_data)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))


@router.put("/password")
async def update_user_password(
        password_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),  #验证token
        db: AsyncSession = Depends(get_database)
):
    res_change_pwd = await user_crud.change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_BAD_REQUEST, detail="修改密码失败")
    return success_response(message="修改密码成功")






