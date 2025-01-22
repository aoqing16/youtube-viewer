@echo off
echo 正在卸载 YouTube 视频查看器服务...

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 已获得管理员权限，继续卸载...
) else (
    echo 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

:: 设置服务名称
set SERVICE_NAME=YouTubeViewer

:: 停止服务
echo 正在停止服务...
net stop %SERVICE_NAME%

:: 下载NSSM（如果需要）
if not exist "nssm\nssm-2.24\win64\nssm.exe" (
    echo 正在下载NSSM...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'}"
    powershell -Command "& {Expand-Archive -Path 'nssm.zip' -DestinationPath 'nssm' -Force}"
)

:: 删除服务
echo 正在删除服务...
nssm\nssm-2.24\win64\nssm.exe remove %SERVICE_NAME% confirm

:: 清理临时文件
echo 正在清理临时文件...
rd /s /q nssm
del nssm.zip 2>nul

echo 卸载完成！
pause
