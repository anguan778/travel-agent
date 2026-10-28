@echo off
setlocal
set URL=https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
set FILE=C:\Users\anan\Desktop\travel_agent\cloudflared.exe
set PROXY=http://127.0.0.1:7897

:RETRY
curl -L -C - -o "%FILE%" "%URL%" --proxy %PROXY% --connect-timeout 10 --max-time 180 -s
if %ERRORLEVEL%==0 goto DONE
echo 下载中断，3秒后自动续传...
timeout /t 3 /nobreak >nul
goto RETRY

:DONE
echo ===== 下载完成 =====
dir "%FILE%"