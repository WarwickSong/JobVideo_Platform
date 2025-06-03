# app/routers/video.py
# 短视频招聘平台后端 - 视频上传和获取路由

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_DIR = "uploaded_videos"  # 上传文件保存的相对目录
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 如果目录不存在则自动创建

def secure_filename(filename: str) -> str:
    # 简单处理，防止目录遍历攻击，只保留文件名部分
    return os.path.basename(filename)

@router.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    # 视频上传接口
    filename = secure_filename(file.filename)  # 处理文件名，防止安全风险
    file_path = os.path.join(UPLOAD_DIR, filename)  # 拼接保存路径
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # 保存上传的视频文件
    except Exception as e:
        # 文件保存失败时返回 500 错误
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    return {"message": "上传成功", "filename": filename}  # 返回上传结果

@router.get("/videos/{filename}")
def get_video(filename: str):
    # 视频获取接口
    filename = secure_filename(filename)  # 处理文件名，防止安全风险
    file_path = os.path.join(UPLOAD_DIR, filename)  # 拼接文件路径
    if not os.path.exists(file_path):
        # 文件不存在时返回 404 错误
        raise HTTPException(status_code=404, detail="文件未找到")
    return FileResponse(file_path, media_type="video/mp4")  # 返回视频文件内容

