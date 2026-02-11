#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查视频表结构脚本

功能：
- 连接到 SQLite 数据库并查看 videos 表的详细结构
- 列出 videos 表的所有列名和数据类型
- 用于确认表结构是否正确设置

使用场景：
- 当你想了解 videos 表的具体结构时
- 检查列是否已正确添加
- 确认数据类型设置是否合理
"""

import sqlite3

# 连接到 SQLite 数据库文件 (test.db)
# 注意：如果文件不存在，SQLite 会自动创建一个新文件
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("开始检查 videos 表结构...")

# 使用 SQLite 特有的 PRAGMA 命令获取表结构信息
# PRAGMA table_info(table_name) 会返回表的所有列信息
cursor.execute('PRAGMA table_info(videos)')

# 获取查询结果（所有列的信息）
columns = cursor.fetchall()

print('videos 表结构:')
if columns:
    for col in columns:
        # col 是一个元组，包含以下信息：
        # col[0]: 列的序号
        # col[1]: 列名
        # col[2]: 数据类型
        # col[3]: 是否为 NOT NULL (1=是, 0=否)
        # col[4]: 默认值
        # col[5]: 是否为主键 (1=是, 0=否)
        print(f'  {col[1]}: {col[2]}')
else:
    print('videos 表不存在或没有列')

# 关闭数据库连接
conn.close()
print("\n操作完成，数据库连接已关闭")
