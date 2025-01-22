@echo off
echo Downloading Git installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe', 'git_installer.exe')"

echo Installing Git...
start /wait git_installer.exe /VERYSILENT /NORESTART

echo Waiting for installation to complete...
timeout /t 30 /nobreak

echo Installation complete!
echo Please close this window and open a new command prompt to continue.
pause
