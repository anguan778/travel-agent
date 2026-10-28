@echo off
set PATH=%PATH%;C:\Program Files\Git\cmd
cd /d C:\Users\anan\Desktop\travel_agent

echo ===== RETRY PUSH 1 =====
git push -u origin main
if %ERRORLEVEL%==0 goto SUCCESS

echo ===== RETRY PUSH 2 =====
timeout /t 5 /nobreak >nul
git push -u origin main
if %ERRORLEVEL%==0 goto SUCCESS

echo ===== RETRY PUSH 3 =====
timeout /t 5 /nobreak >nul
git push -u origin main
if %ERRORLEVEL%==0 goto SUCCESS

echo ===== ALL RETRIES FAILED =====
exit /b 1

:SUCCESS
echo.
echo ===== PUSH SUCCESSFUL =====