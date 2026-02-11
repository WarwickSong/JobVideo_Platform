$ErrorActionPreference = "Continue"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $projectRoot "jobvideo_backend"
$frontendDir = Join-Path $projectRoot "jobvideo_frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JobVideo_Platform 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPort = 8000
$frontendPort = 5173

$backendRunning = $false
$frontendRunning = $false

try {
    Write-Host "[1/4] 检查后端服务..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$backendPort" -Method Head -TimeoutSec 2 -ErrorAction Stop
        $backendRunning = $true
        Write-Host "  后端服务已在运行 (http://127.0.0.1:$backendPort)" -ForegroundColor Green
    } catch {
        Write-Host "  后端服务未运行，准备启动..." -ForegroundColor Gray
    }

    Write-Host "[2/4] 检查前端服务..." -ForegroundColor Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$frontendPort" -Method Head -TimeoutSec 2 -ErrorAction Stop
        $frontendRunning = $true
        Write-Host "  前端服务已在运行 (http://localhost:$frontendPort)" -ForegroundColor Green
    } catch {
        Write-Host "  前端服务未运行，准备启动..." -ForegroundColor Gray
    }

    Write-Host ""

    if (-not $backendRunning) {
        Write-Host "[3/4] 启动后端服务..." -ForegroundColor Yellow
        $backendScript = {
            param($dir)
            Set-Location $dir
            uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
        }
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { $backendScript } $backendDir" -WindowStyle Normal
        Write-Host "  后端服务启动中..." -ForegroundColor Green
        Start-Sleep -Seconds 3
    }

    if (-not $frontendRunning) {
        Write-Host "[4/4] 启动前端服务..." -ForegroundColor Yellow
        $frontendScript = {
            param($dir)
            Set-Location $dir
            if (-not (Test-Path "node_modules")) {
                Write-Host "  首次运行，正在安装依赖..." -ForegroundColor Yellow
                npm install
            }
            npm run dev
        }
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { $frontendScript } $frontendDir" -WindowStyle Normal
        Write-Host "  前端服务启动中..." -ForegroundColor Green
        Start-Sleep -Seconds 3
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  启动完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "后端服务: http://127.0.0.1:$backendPort" -ForegroundColor White
    Write-Host "前端服务: http://localhost:$frontendPort" -ForegroundColor White
    Write-Host "API 文档:  http://127.0.0.1:$backendPort/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "按 Ctrl+C 可停止本脚本，但不会关闭已启动的服务" -ForegroundColor Gray
    Write-Host ""

    $keepRunning = $true
    while ($keepRunning) {
        Start-Sleep -Seconds 1
    }

} catch {
    Write-Host ""
    Write-Host "启动失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请检查以下事项：" -ForegroundColor Yellow
    Write-Host "1. Python 和 uvicorn 是否已安装？" -ForegroundColor Gray
    Write-Host "2. Node.js 和 npm 是否已安装？" -ForegroundColor Gray
    Write-Host "3. 端口 $backendPort 和 $frontendPort 是否被占用？" -ForegroundColor Gray
    Write-Host ""
    Write-Host "手动启动方式：" -ForegroundColor Yellow
    Write-Host "后端: cd jobvideo_backend && uvicorn app.main:app --reload" -ForegroundColor Gray
    Write-Host "前端: cd jobvideo_frontend && npm install && npm run dev" -ForegroundColor Gray
    Write-Host ""
}
