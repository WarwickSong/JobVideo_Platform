import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE videos ADD COLUMN target_type VARCHAR')
    print('已添加 target_type 列')
except Exception as e:
    print(f'target_type 列可能已存在: {e}')

try:
    cursor.execute('ALTER TABLE videos ADD COLUMN target_id VARCHAR')
    print('已添加 target_id 列')
except Exception as e:
    print(f'target_id 列可能已存在: {e}')

conn.commit()

cursor.execute('PRAGMA table_info(videos)')
columns = cursor.fetchall()

print('\n更新后的 videos 表结构:')
for col in columns:
    print(f'  {col[1]}: {col[2]}')

conn.close()
