#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新视频路径脚本

功能：
- 连接到 SQLite 数据库并更新指定视频的文件路径
- 用于修正视频文件路径或迁移文件存储位置
- 更新后显示所有视频记录，确认修改是否成功

使用场景：
- 当视频文件存储位置改变时
- 修正错误的文件路径
- 测试路径更新功能
"""

import sqlite3

# 连接到 SQLite 数据库文件 (test.db)
# 注意：如果文件不存在，SQLite 会自动创建一个新文件
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("开始更新视频路径...")

# SQL 更新：修改 videos 表中 id=1 的记录的 file_path 字段
# 将路径更新为 "/videos/3444cc98710940e8be6a866007a2fc5f.mp4"
cursor.execute('UPDATE videos SET file_path = "/videos/3444cc98710940e8be6a866007a2fc5f.mp4" WHERE id = 1')

# 提交更改到数据库
conn.commit()
print('已更新视频路径')

# 查询所有视频记录，确认更新是否成功
cursor.execute('SELECT id, title, file_path FROM videos')
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
