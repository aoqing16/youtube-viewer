@echo off
chcp 65001 > nul
echo Installing YouTube Video Viewer Service...

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed...
) else (
    echo Please run this script as Administrator!
    pause
    exit /b 1
)

:: Set service name and description
set SERVICE_NAME=YouTubeViewer
set DISPLAY_NAME=YouTube Video Viewer Service
set DESCRIPTION="YouTube Video Viewer Service - Web interface for viewing YouTube video information"

:: Get Python path
for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i

:: Get current directory
set CURRENT_DIR=%~dp0
set SERVER_SCRIPT=%CURRENT_DIR%server.py

:: Download NSSM
echo Downloading NSSM...
powershell -Command "& {Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'}"
powershell -Command "& {Expand-Archive -Path 'nssm.zip' -DestinationPath 'nssm' -Force}"

:: Install service using NSSM
echo Installing service...
nssm\nssm-2.24\win64\nssm.exe install %SERVICE_NAME% "%PYTHON_PATH%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% AppParameters "%SERVER_SCRIPT%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% DisplayName %DISPLAY_NAME%
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% Description %DESCRIPTION%
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% AppDirectory "%CURRENT_DIR%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% Start SERVICE_AUTO_START

:: Start service
echo Starting service...
net start %SERVICE_NAME%

:: Clean up temporary files
echo Cleaning up...
rd /s /q nssm
del nssm.zip

echo Installation complete! Service is running.
echo You can access the viewer at: http://localhost:8000
echo.
echo The service will start automatically when Windows starts.
echo You can manage the service in Windows Services Manager.
pause
