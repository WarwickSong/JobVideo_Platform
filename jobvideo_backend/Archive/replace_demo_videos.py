#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用本地 demo 视频替换数据库中的视频记录

功能：
  1. 将 video 目录下的视频复制到 video_storage
  2. 清空数据库原有视频记录（及关联的浏览/点赞/收藏数据）
  3. 插入新的视频记录，指向复制后的本地文件
"""

import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Windows 控制台编码修正，确保中文输出正常
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sqlalchemy.orm import Session
from app.db import engine, Base
from app.auth.models import User
from app.video.models import Video
from app.interactions.models import VideoView, VideoLike, VideoFavorite
from app.config import settings

# 源视频目录
SOURCE_DIR = r"C:\Coding\JobVideo_Platform\video"
# 目标存储目录
TARGET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.VIDEO_STORAGE_DIR)

os.makedirs(TARGET_DIR, exist_ok=True)

# 每个视频的中文标题和描述说明
# owner 指定上传者角色：employer（招聘方）/ seeker（求职者展示）
VIDEO_METADATA = [
    {"title": "叉车司机精准操控", "description": "叉车司机岗位技能展示，精准操控叉车完成货物搬运", "owner": "seeker"},
    {"title": "建筑工地大桶水搬运", "description": "建筑工地大桶水搬运工作实拍，体力岗位招聘", "owner": "employer"},
    {"title": "建筑工地小桶水搬运", "description": "建筑工地小桶水搬运工作实拍，轻松上手", "owner": "employer"},
    {"title": "快递分拣招聘", "description": "快递分拣岗位工作展示，高效分拣流程一览", "owner": "employer"},
    {"title": "月嫂技能展示", "description": "专业月嫂技能展示，新生儿护理与产妇照料", "owner": "seeker"},
    {"title": "电子厂仓库招聘", "description": "电子厂仓库岗位招聘，仓储管理与物料整理", "owner": "employer"},
    {"title": "电焊工硬核技能", "description": "电焊工技能展示，专业焊接工艺实操", "owner": "seeker"},
    {"title": "直播带货技能展示", "description": "直播带货岗位技能展示，主播话术与产品展示", "owner": "seeker"},
    {"title": "短视频剪辑师职场", "description": "短视频剪辑师日常工作展示，剪辑技巧与创意", "owner": "seeker"},
    {"title": "酒店招聘", "description": "酒店服务岗位招聘，前台客房餐饮多岗位展示", "owner": "employer"},
    {"title": "餐饮招聘", "description": "餐饮行业岗位招聘，厨师服务员后厨岗位展示", "owner": "employer"},
]


def copy_videos():
    """将源目录的视频文件复制到 video_storage"""
    print("=== 复制视频文件 ===")
    copied = []
    for fname in os.listdir(SOURCE_DIR):
        if not fname.endswith(".mp4"):
            continue
        src = os.path.join(SOURCE_DIR, fname)
        dst = os.path.join(TARGET_DIR, fname)
        shutil.copy2(src, dst)
        copied.append(fname)
        print(f"  ✔ {fname}")
    print(f"共复制 {len(copied)} 个视频\n")
    return copied


def replace_video_data(video_files):
    """清空旧数据，插入新视频记录"""
    print("=== 替换数据库视频记录 ===")

    with Session(engine) as session:
        # 查找上传者用户
        employer = session.query(User).filter(User.username == "demo_employer").first()
        seeker = session.query(User).filter(User.username == "demo_seeker").first()
        if not employer or not seeker:
            print("❌ 未找到 demo_employer 或 demo_seeker 用户，请先运行 create_demo_users.py")
            sys.exit(1)

        owner_map = {
            "employer": employer.id,
            "seeker": seeker.id,
        }

        # 统计旧数据
        old_videos = session.query(Video).count()
        old_views = session.query(VideoView).count()
        old_likes = session.query(VideoLike).count()
        old_favorites = session.query(VideoFavorite).count()
        print(f"旧数据：{old_videos} 视频, {old_views} 浏览, {old_likes} 点赞, {old_favorites} 收藏")

        # 清空关联数据（注意外键顺序：先删引用方）
        session.query(VideoView).delete()
        session.query(VideoLike).delete()
        session.query(VideoFavorite).delete()
        session.query(Video).delete()
        session.flush()

        # 插入新视频记录
        for fname, meta in zip(video_files, VIDEO_METADATA):
            video = Video(
                title=meta["title"],
                description=meta["description"],
                filename=fname,
                file_path=f"/videos/{fname}",
                owner_id=owner_map[meta["owner"]],
            )
            session.add(video)

        session.commit()

        new_count = session.query(Video).count()
        print(f"插入 {new_count} 个新视频记录")
        print("替换完成！\n")


def main():
    video_files = copy_videos()

    if not video_files:
        print("❌ 源目录中未找到 .mp4 视频文件")
        sys.exit(1)

    expected = len(VIDEO_METADATA)
    if len(video_files) != expected:
        print(f"⚠ 源目录有 {len(video_files)} 个视频，但元数据定义了 {expected} 个")
        print("请检查 video 目录下的文件是否完整")
        sys.exit(1)

    # 按文件名排序，确保与元数据顺序一致
    video_files.sort()
    replace_video_data(video_files)

    print("=== 全部完成 ===")
    print("请重启后端服务以生效")


if __name__ == "__main__":
    main()
