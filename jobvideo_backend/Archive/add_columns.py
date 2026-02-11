#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加视频表的目标绑定字段脚本

功能：
- 向 videos 表添加 target_type 和 target_id 列
- 用于实现视频与其他业务对象（如职位、简历、公司介绍）的绑定
- 这些列是实现视频通用绑定功能的核心字段

使用场景：
- 当你需要为视频添加绑定其他对象的能力时运行
- 首次设置数据库结构时使用
"""

import sqlite3

# 连接到 SQLite 数据库文件 (test.db)
# 注意：如果文件不存在，SQLite 会自动创建一个新文件
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("开始添加视频绑定字段...")

# 尝试添加 target_type 列（目标类型）
try:
    # SQL 语句：修改 videos 表，添加 target_type 列，类型为 VARCHAR (字符串)
    cursor.execute('ALTER TABLE videos ADD COLUMN target_type VARCHAR')
    print('已添加 target_type 列 (用于存储绑定对象类型，如 job/resume/company_intro)')
except Exception as e:
    # 如果列已存在，会捕获异常并提示
    print(f'target_type 列可能已存在: {e}')

# 尝试添加 target_id 列（目标ID）
try:
    # SQL 语句：修改 videos 表，添加 target_id 列，类型为 VARCHAR (字符串)
    cursor.execute('ALTER TABLE videos ADD COLUMN target_id VARCHAR')
    print('已添加 target_id 列 (用于存储绑定对象的ID)')
except Exception as e:
    # 如果列已存在，会捕获异常并提示
    print(f'target_id 列可能已存在: {e}')

# 提交所有更改到数据库
conn.commit()
print("更改已保存到数据库")

# 查看更新后的表结构
# PRAGMA table_info 是 SQLite 特有的命令，用于获取表的列信息
cursor.execute('PRAGMA table_info(videos)')
columns = cursor.fetchall()

print('\n更新后的 videos 表结构:')
for col in columns:
    # col 是一个元组，包含列的信息：(id, name, type, notnull, default_value, pk)
    # 这里我们只打印列名和类型
    print(f'  {col[1]}: {col[2]}')

# 关闭数据库连接
conn.close()
print("\n操作完成，数据库连接已关闭")
