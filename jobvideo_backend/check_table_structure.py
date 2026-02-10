import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(videos)')
columns = cursor.fetchall()

print('videos 表结构:')
for col in columns:
    print(f'  {col[1]}: {col[2]}')

conn.close()
