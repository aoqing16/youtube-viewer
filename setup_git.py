import subprocess
import os
import sys

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"成功: {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"失败: {command}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def setup_git():
    print("开始配置Git...")
    
    # 检查git是否安装
    if not run_command("git --version"):
        print("请先安装Git！")
        return False
    
    # 初始化git仓库
    if not os.path.exists(".git"):
        if not run_command("git init"):
            return False
    
    # 配置用户信息
    commands = [
        'git config user.name "aoqing16"',
        'git config user.email "aoqing16@github.com"',
        'git remote remove origin',
        'git remote add origin https://github.com/aoqing16/youtube-viewer.git',
        'git add youtube_videos.json index.html',
        'git status'
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    print("\nGit配置完成！")
    return True

if __name__ == "__main__":
    setup_git()
