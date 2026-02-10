import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('SELECT id, title, file_path FROM videos')
rows = cursor.fetchall()

print('视频记录:')
if rows:
    for r in rows:
        print(f'ID: {r[0]}, 标题: {r[1]}, 路径: {r[2]}')
else:
    print('没有视频记录')

conn.close()
