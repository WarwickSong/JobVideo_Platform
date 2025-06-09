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
$env:DATABASE_URL = "sqlite:///./test.db"
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

# 登录获取 Token
# 使用 curl 命令登录获取 Token
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "123456"}'
# 使用 PowerShell 登录获取 Token
Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "alice", "password": "123456"}'
# Token 过长的解决方法
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "alice", "password": "123456"}'

$response  # 这样会完整显示返回内容

# 用 Token 访问用户信息
# 使用 curl 命令访问用户信息
curl http://localhost:8000/auth/me -H "Authorization: Bearer <你的token>"
# 使用 PowerShell 访问用户信息
Invoke-RestMethod -Uri "http://localhost:8000/auth/me" `
  -Headers @{ "Authorization" = "Bearer <你的token>" }

Invoke-RestMethod -Uri "http://localhost:8000/auth/me" `
  -Headers @{ "Authorization" = "Bearer $($response.access_token)" }
