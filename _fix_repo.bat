@echo off
set PATH=%PATH%;C:\Program Files\Git\cmd
cd /d C:\Users\anan\Desktop\travel_agent

git rm -r --cached __pycache__ 2>nul
git rm --cached _setup_git.bat 2>nul
git add .gitignore
git add -A
git commit --amend -m "travel agent initial version"
echo.
echo ===== REPO CLEANED =====
git log --oneline
git ls-files