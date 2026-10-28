@echo off
set PATH=%PATH%;C:\Program Files\Git\cmd
cd /d C:\Users\anan\Desktop\travel_agent

git remote remove origin 2>nul
git remote add origin https://github.com/anguan778/travel-agent.git
git branch -M main
echo.
echo ===== PUSHING TO GITHUB =====
echo If a browser window opens, please log in to GitHub to authorize.
echo.
git push -u origin main
echo.
echo ===== PUSH RESULT: %ERRORLEVEL% =====