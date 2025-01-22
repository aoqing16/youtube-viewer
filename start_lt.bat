@echo off
echo Starting local server and tunnel...

:: Kill any existing Python server
taskkill /F /IM pythonw.exe >nul 2>&1

:: Start the local server
start /B pythonw server.py

:: Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak > nul

:: Start the tunnel
echo Starting tunnel...
echo Your public URL will be shown below:
echo.
lt --port 8000

pause
