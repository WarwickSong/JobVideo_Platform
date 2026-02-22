$ErrorActionPreference = "Continue"

# Configuration variables
$CONDA_ENV_NAME = "jobvideo-backend"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $projectRoot "jobvideo_backend"
$frontendDir = Join-Path $projectRoot "jobvideo_frontend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  JobVideo_Platform Launch Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Using conda environment: $CONDA_ENV_NAME" -ForegroundColor Yellow
Write-Host ""

$backendPort = 8000
$frontendPort = 5173

# Check backend service
Write-Host "[1/4] Checking backend service..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:$backendPort" -Method Head -TimeoutSec 2 -ErrorAction Stop -UseBasicParsing
    Write-Host "  Backend service is already running (http://127.0.0.1:$backendPort)" -ForegroundColor Green
} catch {
    Write-Host "  Backend service is not running, starting..." -ForegroundColor Gray
    # Start backend service
    Write-Host "[3/4] Starting backend service..." -ForegroundColor Yellow
    $backendCommand = "conda activate $CONDA_ENV_NAME; Set-Location '$backendDir'; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -WindowStyle Normal
    Write-Host "  Backend service starting..." -ForegroundColor Green
    Start-Sleep -Seconds 3
}

# Check frontend service
Write-Host "[2/4] Checking frontend service..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:$frontendPort" -Method Head -TimeoutSec 2 -ErrorAction Stop -UseBasicParsing
    Write-Host "  Frontend service is already running (http://localhost:$frontendPort)" -ForegroundColor Green
} catch {
    Write-Host "  Frontend service is not running, starting..." -ForegroundColor Gray
    # Start frontend service
    Write-Host "[4/4] Starting frontend service..." -ForegroundColor Yellow
    $frontendCommand = "Set-Location '$frontendDir'; if (-not (Test-Path 'node_modules')) { npm install }; npm run dev"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand -WindowStyle Normal
    Write-Host "  Frontend service starting..." -ForegroundColor Green
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Launch Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend: http://127.0.0.1:$backendPort" -ForegroundColor White
Write-Host "Frontend: http://localhost:$frontendPort" -ForegroundColor White
Write-Host "API Docs: http://127.0.0.1:$backendPort/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray

# Wait for user input
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
