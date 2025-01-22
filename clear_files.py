import os
import sys

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

files_to_delete = ['youtube_videos.json', 'index.html']

for file in files_to_delete:
    if os.path.exists(file):
        try:
            os.remove(file)
            print(f"已删除: {file}")
        except Exception as e:
            print(f"删除失败 {file}: {str(e)}")
    else:
        print(f"文件不存在: {file}")

print("\n清理完成!")
