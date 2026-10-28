@echo off
chcp 65001 >nul
title 旅游攻略助手 - 云端部署
echo ============================================
echo   旅游攻略助手「游游」- 一键上云启动
echo ============================================
echo.

:: 检查 cloudflared 是否存在
if not exist "%~dp0cloudflared.exe" (
    echo [错误] 未找到 cloudflared.exe，请先运行 _download_cf.bat 下载
    pause
    exit /b 1
)

:: 启动 Flask 应用（后台）
echo [1/2] 正在启动 Flask 应用...
start /b "" python "%~dp0app.py" >nul 2>&1
timeout /t 3 /nobreak >nul

:: 启动 cloudflared 隧道（前台，保持运行）
echo [2/2] 正在启动 cloudflared 隧道...
echo.
echo 公网URL将在下方显示（每次启动URL会变化）
echo 关闭此窗口即可停止服务
echo ============================================
echo.
"%~dp0cloudflared.exe" tunnel --url http://localhost:8080