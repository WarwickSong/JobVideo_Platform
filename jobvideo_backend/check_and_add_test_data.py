#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构并添加测试数据的脚本
"""

import os
import sys
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import engine, Base
from app.video.models import Video
from app.auth.models import User


def check_tables():
    """检查数据库表结构"""
    print("=== 检查数据库表结构 ===")
    inspector = inspect(engine)
    
    # 获取所有表名
    tables = inspector.get_table_names()
    print(f"数据库中的表: {tables}")
    
    # 检查video表
    if 'videos' in tables:
        print("\n=== videos表结构 ===")
        columns = inspector.get_columns('videos')
        for column in columns:
            print(f"  {column['name']}: {column['type']}")
    
    # 检查users表
    if 'users' in tables:
        print("\n=== users表结构 ===")
        columns = inspector.get_columns('users')
        for column in columns:
            print(f"  {column['name']}: {column['type']}")


def add_test_data():
    """添加测试数据"""
    print("\n=== 添加测试数据 ===")
    
    # 创建会话
    with Session(engine) as session:
        # 检查是否已有用户
        user = session.query(User).first()
        if not user:
            # 创建测试用户
            user = User(
                username="testuser",
                phone="13800138000",
                password_hash="testpassword"  # 实际应用中应该哈希处理
            )
            session.add(user)
            session.commit()
            print("已创建测试用户: testuser")
        else:
            print(f"已存在用户: {user.username}")
        
        # 检查是否已有视频
        video_count = session.query(Video).count()
        print(f"当前视频数量: {video_count}")
        
        if video_count == 0:
            # 创建测试视频
            test_videos = [
                {
                    "title": "测试视频1",
                    "description": "这是第一个测试视频",
                    "file_path": "https://media.w3.org/2010/05/sintel/trailer.mp4",
                    "filename": "test_video_1.mp4",
                    "owner_id": user.id
                },
                {
                    "title": "测试视频2", 
                    "description": "这是第二个测试视频",
                    "file_path": "https://vjs.zencdn.net/v/oceans.mp4",
                    "filename": "test_video_2.mp4",
                    "owner_id": user.id
                },
                {
                    "title": "测试视频3",
                    "description": "这是第三个测试视频",
                    "file_path": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
                    "filename": "test_video_3.mp4",
                    "owner_id": user.id
                },
                {
                    "title": "测试视频4",
                    "description": "这是第四个测试视频",
                    "file_path": "https://www.w3schools.com/html/movie.mp4",
                    "filename": "test_video_4.mp4",
                    "owner_id": user.id
                }
            ]
            
            for video_data in test_videos:
                video = Video(**video_data)
                session.add(video)
            
            session.commit()
            print(f"已添加 {len(test_videos)} 个测试视频")
        else:
            print("已有视频数据，跳过添加测试视频")


def main():
    """主函数"""
    try:
        check_tables()
        add_test_data()
        print("\n=== 操作完成 ===")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
