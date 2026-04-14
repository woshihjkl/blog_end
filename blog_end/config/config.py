from typing import Final

# 数据库配置
ASYNC_DATABASE_URL: Final[str] = "mysql+aiomysql://root:123456@localhost:3306/blog"

# JWT 配置 (临时明文版，后面再改)
SECRET_KEY: Final[str] = "your-secret-key-change-in-production"
ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 10080