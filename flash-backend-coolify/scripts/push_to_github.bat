@echo off
echo ========================================
echo PUSH TO GITHUB
echo ========================================
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (e.g., flash-erp-backend): "

echo.
echo Adding remote repository...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo DONE! Check your repository at:
echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo ========================================
pause
