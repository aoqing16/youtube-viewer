import subprocess
import sys
import time
import os

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Git可执行文件的完整路径
GIT_PATH = r"C:\Program Files\Git\cmd\git.exe"

def run_command(command):
    try:
        # 替换命令中的git为完整路径
        if command.startswith('git '):
            command = f'"{GIT_PATH}" {command[4:]}'
        
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

def push_to_github():
    print("开始推送到GitHub...")
    
    if not os.path.exists(GIT_PATH):
        print(f"错误: Git不在预期位置 ({GIT_PATH})")
        print("请确保Git已正确安装")
        return False
    
    commands = [
        # 确保我们在main分支上
        'git checkout main',
        # 添加所有文件
        'git add .',
        # 提交更改
        f'git commit -m "Update videos: {time.strftime("%Y-%m-%d %H:%M:%S")}"',
        # 强制推送到main分支
        'git push -f origin main'
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    print("\n✅ 成功推送到GitHub！")
    print("\n请确保在GitHub仓库设置中：")
    print("1. 进入 Settings > Pages")
    print("2. Source 选择 'Deploy from a branch'")
    print("3. Branch 选择 'main' 分支，文件夹选择 '/ (root)'")
    print("4. 点击 Save")
    return True

if __name__ == "__main__":
    push_to_github()
