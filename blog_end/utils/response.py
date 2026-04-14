from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message : str = "success", data = None):
    """构造成功响应"""
    # 构造统一响应格式
    content = {
        "code" : 200,
        "message" : message,
        "data" : data
    }
#确保Fastapi、pydantic、orm对象都正常响应
    return JSONResponse(content = jsonable_encoder(content))


