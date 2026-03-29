# app/config.py
# 应用配置文件
# 功能：统一管理应用的配置参数，包括密钥、数据库连接等

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# 如果你不使用 .env，也可以直接在代码中写入字符串
load_dotenv()


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]

class Settings:
    # JWT密钥，建议后期写入 .env 文件以提高安全性
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    
    # JWT加密算法
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # 访问令牌过期时间（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # 数据库连接URL
    # 默认使用本地SQLite数据库
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # 视频文件存储目录
    VIDEO_STORAGE_DIR: str = os.getenv("VIDEO_STORAGE_DIR", "video_storage")
    APP_ENV: str = os.getenv("APP_ENV", "development").lower()
    ENABLE_TEST_TOKEN: bool = os.getenv("ENABLE_TEST_TOKEN", "true").lower() == "true"
    FRONTEND_ORIGINS: list[str] = _split_csv(
        os.getenv("FRONTEND_ORIGINS", "http://localhost:5173")
    )

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def cors_allow_origins(self) -> list[str]:
        if self.is_production:
            return self.FRONTEND_ORIGINS or []
        return ["*"]

# 创建配置实例
# 其他模块通过导入这个settings对象来访问配置
settings = Settings()
