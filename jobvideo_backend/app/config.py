# app/config.py  统一配置文件

import os
from dotenv import load_dotenv

# 如果你不使用 .env，也可以直接写入字符串
load_dotenv()  # 加载 .env 文件（可选）

class Settings:
    # 密钥建议后期写入 .env 文件
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 数据库连接（默认本地 SQLite）
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # 视频文件存储目录
    VIDEO_STORAGE_DIR: str = "video_storage"

settings = Settings()
