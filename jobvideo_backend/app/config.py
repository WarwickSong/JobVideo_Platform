# app/config.py
# 应用配置文件
# 功能：统一管理应用的配置参数，包括密钥、数据库连接等

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# 如果你不使用 .env，也可以直接在代码中写入字符串
load_dotenv()

class Settings:
    # JWT密钥，建议后期写入 .env 文件以提高安全性
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    
    # JWT加密算法
    ALGORITHM: str = "HS256"
    
    # 访问令牌过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 数据库连接URL
    # 默认使用本地SQLite数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # 视频文件存储目录
    VIDEO_STORAGE_DIR: str = "video_storage"

# 创建配置实例
# 其他模块通过导入这个settings对象来访问配置
settings = Settings()
