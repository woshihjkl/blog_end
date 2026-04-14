import traceback

from fastapi import  HTTPException,Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

DEBUG_MODE = True  #开始调试


#业务层面
async  def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP异常处理
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code" : exc.status_code,
            "message": exc.detail,
            "data" : None
        }
    )

#数据库完整性约束
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    数据库异常处理
    """
    error_msg = str(exc.orig)

    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg :
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，检查输入"

        #开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_typr": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }


    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": None
        }
    )

#处理SQLALchemy 数据库错误
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    数据库异常处理
    """
    #开发模式下返回详细错误信息
    error_data =  None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),  #格式化异常信息为字符串
            "path": str(request.url)
        }


    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，稍后再试",
            "data": error_data
        }
    )


async  def general_exception_handler(request: Request, exc: Exception):
    """
    其他异常处理
    """
    #开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),  #格式化异常信息为字符串
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库内部错误",
            "data": error_data
        }
    )
