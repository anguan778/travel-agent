@echo off
set PATH=%PATH%;C:\Program Files\Git\cmd
cd /d C:\Users\anan\Desktop\travel_agent

echo ===== CONFIGURING GIT PROXY =====
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897

echo ===== PUSHING VIA PROXY =====
git push -u origin main
echo.
echo ===== PUSH RESULT: %ERRORLEVEL% =====