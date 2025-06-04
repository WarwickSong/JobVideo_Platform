# app/main.py
# 项目主入口，创建 FastAPI 应用并注册路由

from fastapi import FastAPI
from app.routers import video, job  # 导入视频相关路由

app = FastAPI()  # 创建 FastAPI 应用实例
app.include_router(video.router)  # 注册视频路由
app.include_router(job.router)

@app.get("/")
def read_root():
    # 根路径接口，返回服务运行状态
    return {"message": "短视频招聘平台后端运行中"}
