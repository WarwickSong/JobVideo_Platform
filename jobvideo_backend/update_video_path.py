import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('UPDATE videos SET file_path = "/videos/3444cc98710940e8be6a866007a2fc5f.mp4" WHERE id = 1')
conn.commit()

print('已更新视频路径')

cursor.execute('SELECT id, title, file_path FROM videos')
rows = cursor.fetchall()

print('视频记录:')
for r in rows:
    print(f'ID: {r[0]}, 标题: {r[1]}, 路径: {r[2]}')

conn.close()
