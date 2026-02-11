#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库表结构脚本

功能：
- 连接到 SQLite 数据库并列出所有表名
- 用于快速查看数据库中有哪些表
- 适合在开发或调试时使用

使用场景：
- 当你想了解数据库结构时
- 检查数据库初始化是否成功
- 确认表是否已正确创建
"""

import sqlite3

# 连接到 SQLite 数据库文件 (test.db)
# 注意：如果文件不存在，SQLite 会自动创建一个新文件
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

print("开始检查数据库表...")

# SQL 查询：从 sqlite_master 表中获取所有表的名称
# sqlite_master 是 SQLite 内置的系统表，存储数据库的元数据
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# 获取查询结果（所有表名）
tables = cursor.fetchall()

print('数据库表:')
if tables:
    for t in tables:
        # t 是一个元组，第一个元素是表名
        print(f'- {t[0]}')
else:
    print('数据库中没有表')

# 关闭数据库连接
conn.close()
print("\n操作完成，数据库连接已关闭")
