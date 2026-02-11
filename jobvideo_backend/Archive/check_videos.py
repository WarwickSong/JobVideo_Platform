#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查视频记录脚本

功能：
- 连接到 SQLite 数据库并查询 videos 表中的所有记录
- 显示视频的 ID、标题和文件路径
- 用于查看数据库中的视频数据

使用场景：
- 当你想查看数据库中有哪些视频时
- 检查视频上传是否成功
- 确认视频数据是否正确存储
"""

import sqlite3

# 连接到 SQLite 数据库文件 (test.db)
# 注意：如果文件不存在，SQLite 会自动创建一个新文件
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("开始检查视频记录...")

# SQL 查询：从 videos 表中选择 id、title、file_path 列
# 这些是视频的基本信息字段
cursor.execute('SELECT id, title, file_path FROM videos')

# 获取查询结果（所有视频记录）
rows = cursor.fetchall()

print('视频记录:')
if rows:
    for r in rows:
        # r 是一个元组，包含以下字段：
        # r[0]: 视频 ID
        # r[1]: 视频标题
        # r[2]: 视频文件路径
        print(f'ID: {r[0]}, 标题: {r[1]}, 路径: {r[2]}')
else:
    print('没有视频记录')

# 关闭数据库连接
conn.close()
print("\n操作完成，数据库连接已关闭")
