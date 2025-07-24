# app/main.py
# 项目主入口，创建 FastAPI 应用并注册路由

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.video import routes as video_routes
from app.routers import video, job  # 导入视频相关路由
from app.auth import routes as auth_routes
from app.db import Base, engine
from app.job import models as job_models
from app.video import models as video_models
from app.job import routes as job_routes

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
