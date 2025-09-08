# 视频保存等辅助函数
# app/video/utils.py

import os
import uuid
import shutil
import asyncio

from typing import Optional
from functools import partial
from fastapi import UploadFile, HTTPException
from concurrent.futures import ThreadPoolExecutor

from app.config import settings

# 配置参数
VIDEO_STORAGE_DIR = settings.VIDEO_STORAGE_DIR
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB
VALID_CONTENT_TYPES = {
    "video/mp4",
    "video/webm",
    "video/quicktime",
}

# 创建线程池用于执行阻塞操作
thread_pool = ThreadPoolExecutor(max_workers=4)

async def save_video_file(file: UploadFile) -> str:
    # 验证文件类型
    if file.content_type not in VALID_CONTENT_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的视频格式: {file.content_type}"
        )
    
    # 根据Content-Type确定正确的文件扩展名
    CONTENT_TYPE_MAPPING = {
        "video/mp4": ".mp4",
        "video/webm": ".webm",
        "video/quicktime": ".mov",
    }
    ext = CONTENT_TYPE_MAPPING.get(file.content_type, ".mp4")
    
    # 生成带正确扩展名的唯一文件名
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(VIDEO_STORAGE_DIR, filename)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 异步流式写入文件
    try:
        total_size = 0
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                total_size += len(chunk)
                
                # 检查文件大小限制
                if total_size > MAX_VIDEO_SIZE:
                    os.remove(file_path)
                    raise HTTPException(
                        status_code=413, 
                        detail=f"视频大小超过限制 ({MAX_VIDEO_SIZE / (1024*1024):.1f} MB)"
                    )
                
                # 使用线程池执行阻塞写入操作
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(
                    thread_pool, 
                    partial(buffer.write, chunk)
                )
        
        # 可选：异步生成缩略图
        # await generate_thumbnail(file_path)
        
        return file_path
    
    except Exception as e:
        # 发生错误时清理不完整文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"上传失败: {str(e)}"
        )
    finally:
        await file.close()    
