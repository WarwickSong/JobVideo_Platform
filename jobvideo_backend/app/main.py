# app/main.py
# 项目主入口，创建 FastAPI 应用并注册路由

# 第三方库导入
import traceback
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 本地应用路由, 数据库相关导入
from app.db import Base, engine
from app.auth import routes as auth_routes
from app.job import routes as job_routes
from app.job import models as job_models
from app.video import routes as video_routes
from app.video import models as video_models


# 初始化数据库表
Base.metadata.create_all(bind=engine)  # 创建所有表结构

app = FastAPI()  # 创建 FastAPI 应用实例

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory="uploaded_videos"), name="videos")  # 静态文件目录，用于存放上传的视频文件
app.include_router(job_routes.router)  # 注册工作相关路由
app.include_router(video_routes.router)  # 注册视频相关路由
app.include_router(auth_routes.router)  # 注册认证相关路由

@app.get("/")
def read_root():
    # 根路径接口，返回服务运行状态
    return {"message": "短视频招聘平台后端运行中"}


# 添加全局异常处理器
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"Error processing request: {exc}")
    traceback.print_exc()  # 打印完整堆栈信息
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )
