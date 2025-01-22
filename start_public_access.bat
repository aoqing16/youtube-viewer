@echo off
echo Starting ngrok tunnel...

:: Kill any existing ngrok processes
taskkill /F /IM ngrok.exe >nul 2>&1

:: Start ngrok in the background
start /B ngrok http 8000

:: Wait a moment for ngrok to start
timeout /t 5 /nobreak > nul

:: Get the public URL
echo Your public URL is:
for /f "tokens=2 delims=:" %%a in ('curl -s http://127.0.0.1:4040/api/tunnels ^| findstr "public_url"') do (
    echo https:%%a
)

echo.
echo Press Ctrl+C to stop the tunnel...
pause > nul
