from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



class UserCreate(BaseModel):
    """注册/登录时的请求体"""
    username: str
    password: str


class UserResponse(BaseModel):
    """返回给前端的用户信息（不含密码）"""
    id: int
    username: str
    create_time: datetime
    bio: str | None = None
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)

    # user_info对应的类
class UserInfoBase(BaseModel):

   # 用户信息基础数据模型
    nickname: Optional[str] = Field(None , max_length = 50, description = "昵称")
    avatar: Optional[str] = Field(None, max_length = 255, description = "用户头像URL")
    bio: Optional[str] = Field(None, max_length = 500, description = "个人简介")
    gender: Optional[int] = Field(None, max_length=10,description = "性别")

class UserInfoResponse(UserInfoBase):
    # 用户信息返回模型
    id : int
    username : str

    model_config = ConfigDict(
        from_attributes=True  # 允许从ORM对象属性中取值
    )


    # data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(...,alias="user_info")

    model_config = ConfigDict(
        populate_by_name=True,    #alias / 字段名兼容
        from_attributes=True     # 允许从ORM对象属性中取值
    )


#更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像URL")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    gender: Optional[int] = Field(None, max_length=10, description="性别")


#修改密码
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6,alias="newPassword", description="新密码")
