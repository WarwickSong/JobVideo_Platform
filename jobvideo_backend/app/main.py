# app/main.py
# 项目主入口，创建 FastAPI 应用并注册路由

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from app.video import routes as video_routes
from app.routers import video, job  # 导入视频相关路由
from app.auth import routes as auth_routes
from app.db import Base, engine
from app.job import models as job_models
from app.video import models as video_models
from app.job import routes as job_routes
from fastapi.responses import JSONResponse
import traceback

# 初始化数据库表
Base.metadata.create_all(bind=engine)  # 创建所有表结构

app = FastAPI()  # 创建 FastAPI 应用实例
app.mount("/videos", StaticFiles(directory="uploaded_videos"), name="videos")  # 静态文件目录，用于存放上传的视频文件
app.include_router(job_routes.router)  # 注册工作相关路由
app.include_router(video_routes.router)  # 注册视频相关路由
app.include_router(video.router)  # 注册视频路由
app.include_router(job.router)  # 注册工作路由
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

# 导入路由（确保在异常处理器之后导入）
from app.video.routes import router as video_router
app.include_router(video_router, prefix="/video")
