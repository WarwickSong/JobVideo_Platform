# app/main.py
# 项目主入口文件
# 功能：创建 FastAPI 应用实例，配置中间件，注册所有路由，启动后端服务

# 第三方库导入
import traceback
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 本地应用导入
# 数据库基础配置
from app.db import Base, engine
# 各个模块的路由
from app.auth import routes as auth_routes  # 认证模块路由（登录、注册等）
from app.job import routes as job_routes  # 职位模块路由
from app.video import routes as video_routes  # 视频模块路由
from app.interactions import routes as interactions_routes  # 交互行为模块路由
# 模型导入（确保在创建表结构时能找到所有模型）
from app.job import models as job_models  # 职位相关模型
from app.video import models as video_models  # 视频相关模型


# 初始化数据库表结构
# 这行代码会自动创建所有继承自Base的模型对应的数据库表
# 当数据库中不存在这些表时，会自动创建
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
# FastAPI 是一个现代、快速（高性能）的 Python Web 框架
app = FastAPI()

# 配置 CORS 中间件
# CORS (Cross-Origin Resource Sharing) 是一种允许跨域请求的机制
# 这里的配置允许所有来源的请求访问我们的 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求
    allow_credentials=True,  # 允许携带认证信息（如 cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET, POST, PUT, DELETE 等）
    allow_headers=["*"],  # 允许所有请求头
)

# 挂载静态文件目录
# 用于存储和访问上传的视频文件
# 当访问 /videos 路径时，会从 video_storage 目录中提供静态文件
app.mount("/videos", StaticFiles(directory="video_storage"), name="videos")

# 注册各个模块的路由
# 路由是 API 的端点，用于处理客户端的请求
app.include_router(job_routes.router)  # 注册职位相关路由
app.include_router(video_routes.router)  # 注册视频相关路由
app.include_router(auth_routes.router)  # 注册认证相关路由
app.include_router(interactions_routes.router)  # 注册交互行为相关路由

# 根路径接口
# 当访问网站根目录时，返回服务运行状态
@app.get("/")
def read_root():
    """
    根路径接口：
        返回服务运行状态
    
    Returns:
        dict: 包含服务状态信息的字典
    """
    return {"message": "短视频招聘平台后端运行中"}


# 全局异常处理器
# 捕获所有未被处理的异常，返回统一的错误响应格式
# 这样客户端可以得到结构化的错误信息，而不是服务器的原始错误
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    全局异常处理器：
        捕获所有未被处理的异常，返回统一的错误响应格式
    
    Args:
        request: 请求对象
        exc: 异常对象
    
    Returns:
        JSONResponse: 包含错误信息的JSON响应
    """
    # 打印错误信息到服务器控制台，便于调试
    print(f"Error processing request: {exc}")
    traceback.print_exc()  # 打印完整的错误堆栈信息
    
    # 返回 JSON 格式的错误响应
    return JSONResponse(
        status_code=500,  # HTTP 500 表示服务器内部错误
        content={
            "error": "Internal Server Error",  # 错误类型
            "message": str(exc),  # 具体错误信息
            "type": type(exc).__name__  # 错误的 Python 类型名称
        }
    )
