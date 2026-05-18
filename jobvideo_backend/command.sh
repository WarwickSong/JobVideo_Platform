uvicorn app.main:app --reload

# 创建职位
Invoke-RestMethod -Uri "http://127.0.0.1:8000/jobs/" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"title":"后端工程师", "description":"熟悉 Python", "company":"AI公司", "location":"北京"}'

# 获取所有职位
Invoke-RestMethod -Uri "http://127.0.0.1:8000/jobs/" -Method Get

# 修改职位
Invoke-RestMethod -Uri "http://127.0.0.1:8000/jobs/1" `
  -Method Put `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"title":"后端开发", "description":"精通 FastAPI", "company":"AI公司", "location":"远程"}'

# 删除职位
Invoke-RestMethod -Uri "http://127.0.0.1:8000/jobs/1" -Method Delete

✅ 数据库使用方式总结
📌 本地开发（默认 SQLite）：
# 在 Linux 或 macOS 中设置环境变量并启动应用
DATABASE_URL=sqlite:///./test.db uvicorn app.main:app --reload
# 使用 PowerShell 启动 FastAPI 应用
$env:DATABASE_URL = "sqlite:///../data/jobvideo.db"
uvicorn app.main:app --reload
📌 部署时使用 PostgreSQL：
# 在 Linux 或 macOS 中设置环境变量并启动应用
export DATABASE_URL=postgresql://user:pass@localhost:5432/jobvideo
uvicorn app.main:app
# 使用 PowerShell 启动 FastAPI 应用
$env:DATABASE_URL = "postgresql://user:pass@localhost:5432/jobvideo"
uvicorn app.main:app

# 注册用户
# 使用 curl 命令注册用户
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "a@x.com", "password": "123456", "role": "seeker"}'
# 使用 PowerShell 注册用户
Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "alice", "email": "a@x.com", "password": "123456", "role": "seeker"}'

Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "billy", "email": "b@x.com", "password": "123456", "role": "employer"}'

# 登录获取 Token
# 使用 curl 命令登录获取 Token
"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzMTkzMzgwfQ.0LJemZ0Wsi9teJ_XoV2idTXOwpbElfSwhPj_gBLY2fQ"
"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzUzMTk2MDU5fQ.QY_XqeLPzptOV3ETumHvL2cVJdLfRtT-7rNNW4f_KAM"

curl -X POST http://localhost:8000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"alice\", \"password\": \"123456\"}"
  -d "{\"username\": \"billy\", \"password\": \"123456\"}"
# 使用 PowerShell 登录获取 Token
Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "alice", "password": "123456"}'  # -Body '{"username": "billy", "password": "123456"}'
# Token 过长的解决方法
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "alice", "password": "123456"}'  # -Body '{"username": "billy", "password": "123456"}'

$response  # 这样会完整显示返回内容

# 用 Token 访问用户信息
# 使用 curl 命令访问用户信息
curl http://localhost:8000/auth/me -H "Authorization: Bearer <你的token>"
# 使用 PowerShell 访问用户信息
Invoke-RestMethod -Uri "http://localhost:8000/auth/me" `
  -Headers @{ "Authorization" = "Bearer <你的token>" }

Invoke-RestMethod -Uri "http://localhost:8000/auth/me" `
  -Headers @{ "Authorization" = "Bearer $($response.access_token)" }

# 视频上传测试 
# 使用 Linux 或 CMD 上传视频
curl -X POST "http://localhost:8000/video/upload" ^
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUzMTkzMzgwfQ.0LJemZ0Wsi9teJ_XoV2idTXOwpbElfSwhPj_gBLY2fQ" ^
  -F "title=测试视频" ^
  -F "file=@C:\Users\Zhihua Song\Desktop\工作室\栖下画廊\栖下画廊视频\栖下画廊 艺术史课程视频\AI时代 我们为什么学习艺术史.mp4"
    
{
  "title": "测试视频",
  "id": 1,
  "filename": "3444cc98710940e8be6a866007a2fc5f.mp4",
  "upload_time": "2025-07-22T13:12:58.538531"
}

# 获取视频列表
GET http://localhost:8000/video/feed?skip=0&limit=10  

