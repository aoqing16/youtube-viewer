@echo off
echo Downloading Node.js installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi', 'node_installer.msi')"

echo Installing Node.js...
msiexec /i node_installer.msi /qn

echo Waiting for installation to complete...
timeout /t 30 /nobreak

echo Installing localtunnel...
call npm install -g localtunnel

echo Creating startup script for localtunnel...
(
echo @echo off
echo echo Starting local server and tunnel...
echo start /B pythonw server.py
echo timeout /t 5 /nobreak
echo lt --port 8000
) > start_tunnel.bat

echo Installation complete!
echo Now you can run start_tunnel.bat to create a public URL.
pause
