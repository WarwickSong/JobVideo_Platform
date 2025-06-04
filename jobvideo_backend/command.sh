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

