@echo off
echo Configuring Git...
git config --global user.name "aoqing16"
git config --global user.email "wangchuanbing027@gmail.com"

echo Initializing repository...
git init
git add .
git commit -m "Initial commit"
git branch -M main

echo Adding remote repository...
git remote add origin https://github.com/aoqing16/youtube-viewer.git

echo.
echo Configuration complete! 
echo Please run the following command to push your code:
echo git push -u origin main
echo.
echo After pushing, go to:
echo https://github.com/aoqing16/youtube-viewer/settings/pages
echo And set up GitHub Pages with the following settings:
echo - Source: Deploy from a branch
echo - Branch: gh-pages
echo.
pause
