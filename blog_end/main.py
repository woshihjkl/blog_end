from contextlib import asynccontextmanager
from fastapi import FastAPI
import models
import database
from routers import users, articles,favorite,comment
from utils.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await database.init_db()
    yield
    # 关闭时清理资源
    await database.close_db()

app = FastAPI(lifespan=lifespan)


#注册成功全局异常处理器
register_exception_handlers(app)

# 挂载路由
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(favorite.router)
app.include_router(comment.router)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with Async SQLAlchemy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
