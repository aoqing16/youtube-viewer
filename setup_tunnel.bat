@echo off
echo Setting up tunnel service...

:: 创建一个使用frp的启动脚本
(
echo @echo off
echo echo Starting local server in background...
echo start /B pythonw server.py
echo echo Server started! You can access it at:
echo echo Local: http://localhost:8000
echo echo.
echo echo To make it accessible from the internet, please visit:
echo echo https://www.natfrp.com/
echo echo And follow the instructions to set up a tunnel to port 8000
echo echo.
echo pause
) > start_frp.bat

echo Setup complete!
echo.
echo 由于各种内网穿透工具都不太稳定，建议：
echo 1. 访问 https://www.natfrp.com/
echo 2. 注册一个账号
echo 3. 下载他们的客户端
echo 4. 创建一个隧道，本地端口填写 8000
echo.
echo 这个服务更稳定，而且是中国本地的服务器，访问会更快。
echo.
echo 现在你可以运行 start_frp.bat 来启动本地服务器。
echo.
pause
