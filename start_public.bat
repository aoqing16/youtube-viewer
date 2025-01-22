@echo off
echo Starting public access tunnel...
echo This will create a public URL for your local server.
echo.

:: Check if ssh is available
where ssh >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: SSH client is not installed.
    echo Please install OpenSSH client from Windows Settings ^> Apps ^> Optional features
    pause
    exit /b 1
)

:: Start the tunnel
echo Creating tunnel to localhost:8000...
echo Your public URL will be shown below:
echo.
ssh -R 80:localhost:8000 nokey@localhost.run

echo.
echo Tunnel closed.
pause
