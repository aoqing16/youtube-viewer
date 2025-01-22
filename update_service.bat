@echo off
chcp 65001 > nul
echo Updating YouTube Video Viewer Service configuration...

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed...
) else (
    echo Please run this script as Administrator!
    pause
    exit /b 1
)

:: Set service name
set SERVICE_NAME=YouTubeViewer
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python39\python.exe
set CURRENT_DIR=%~dp0
set SERVER_SCRIPT=%CURRENT_DIR%server.py

:: Download NSSM if not exists
if not exist "nssm\nssm-2.24\win64\nssm.exe" (
    echo Downloading NSSM...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'}"
    powershell -Command "& {Expand-Archive -Path 'nssm.zip' -DestinationPath 'nssm' -Force}"
)

:: Update service configuration
echo Updating service configuration...
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% Application "%PYTHON_PATH%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% AppParameters "%SERVER_SCRIPT%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% AppDirectory "%CURRENT_DIR%"
nssm\nssm-2.24\win64\nssm.exe set %SERVICE_NAME% AppEnvironmentExtra PATH=%PATH%

:: Start service
echo Starting service...
net start %SERVICE_NAME%

:: Clean up
echo Cleaning up...
rd /s /q nssm
del nssm.zip

echo Service configuration updated and service started.
echo You can access the viewer at: http://localhost:8000
pause
