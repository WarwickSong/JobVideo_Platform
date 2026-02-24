# app/video/utils.py
# 视频处理工具函数
# 功能：提供视频上传、编码检查、转码等辅助功能

import os
import uuid
import shutil
import asyncio

from typing import Optional, Tuple
from functools import partial
from fastapi import UploadFile, HTTPException
from concurrent.futures import ThreadPoolExecutor
import ffmpeg

from app.config import settings

# 配置参数
VIDEO_STORAGE_DIR = settings.VIDEO_STORAGE_DIR  # 视频存储目录
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB，文件分块大小
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB，最大视频大小限制
VALID_CONTENT_TYPES = {  # 支持的视频格式
    "video/mp4",
    "video/webm",
    "video/quicktime",
}

# 创建线程池用于执行阻塞操作
# 避免阻塞事件循环，提高并发性能
thread_pool = ThreadPoolExecutor(max_workers=4)


def check_video_codec(video_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    检查视频编码格式函数：
        分析视频文件，提取视频和音频的编码格式
    
    Args:
        video_path: 视频文件路径
    
    Returns:
        Tuple[Optional[str], Optional[str]]: (video_codec, audio_codec) 元组
    """
    try:
        # 使用ffmpeg.probe分析视频文件
        probe = ffmpeg.probe(video_path)
        
        video_codec = None
        audio_codec = None
        
        # 遍历所有流，提取视频和音频编码
        for stream in probe['streams']:
            if stream['codec_type'] == 'video' and video_codec is None:
                video_codec = stream['codec_name']
            elif stream['codec_type'] == 'audio' and audio_codec is None:
                audio_codec = stream['codec_name']
        
        return video_codec, audio_codec
    except Exception:
        return None, None


def is_valid_codec(video_codec: Optional[str], audio_codec: Optional[str]) -> bool:
    """
    检查编码格式是否有效函数：
        验证视频编码是否为标准的 H.264 + AAC 格式
    
    Args:
        video_codec: 视频编码格式
        audio_codec: 音频编码格式
    
    Returns:
        bool: 是否为有效的编码格式
    """
    return video_codec == 'h264' and audio_codec == 'aac'


def transcode_video(input_path: str, output_path: str) -> bool:
    """
    视频转码函数：
        将视频转码为 H.264 + AAC 格式，提高兼容性
    
    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
    
    Returns:
        bool: 转码是否成功
    """
    try:
        # 使用ffmpeg进行转码
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec='libx264',  # 视频编码为H.264
                preset='medium',  # 编码速度和质量平衡
                crf=23,  # 质量参数
                acodec='aac',  # 音频编码为AAC
                audio_bitrate='128k'  # 音频比特率
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True, timeout=600)
        )
        return True
    except ffmpeg.Error:
        return False
    except Exception:
        return False


async def save_video_file(file: UploadFile) -> str:
    """
    保存视频文件函数（异步）：
        处理视频上传，包括文件保存、编码检查和转码
    
    Args:
        file: 上传的视频文件对象
    
    Returns:
        str: 保存后的文件路径
    
    Raises:
        HTTPException: 当文件格式不支持、大小超限或转码失败时抛出异常
    """
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
        
        # 检查视频编码格式
        video_codec, audio_codec = check_video_codec(file_path)
        
        # 如果编码不是 H.264 + AAC，进行转码
        if not is_valid_codec(video_codec, audio_codec):
            transcoded_filename = f"{uuid.uuid4().hex}.mp4"
            transcoded_path = os.path.join(VIDEO_STORAGE_DIR, transcoded_filename)
            
            # 使用线程池执行转码操作
            loop = asyncio.get_running_loop()
            transcode_success = await loop.run_in_executor(
                thread_pool,
                partial(transcode_video, file_path, transcoded_path)
            )
            
            if transcode_success:
                # 转码成功，删除原文件，使用转码后的文件
                os.remove(file_path)
                file_path = transcoded_path
            else:
                # 转码失败，删除文件并抛出异常
                os.remove(file_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"视频编码格式不支持 (视频: {video_codec}, 音频: {audio_codec})，且转码失败。请上传 H.264 + AAC 编码的视频。"
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
