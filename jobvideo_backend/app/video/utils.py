# 视频保存等辅助函数
# app/video/utils.py

import os
import shutil
from uuid import uuid4

UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_video_file(file) -> str:
    filename = f"{uuid4().hex}.mp4"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filename
