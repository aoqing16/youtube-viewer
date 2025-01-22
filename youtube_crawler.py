import yt_dlp
import json
from datetime import datetime
import sys
import webbrowser
from jinja2 import Environment, FileSystemLoader

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class YouTubeChannelCrawler:
    def __init__(self):
        """初始化yt-dlp配置"""
        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': False
        }

    def get_channel_videos(self, channel_url, limit=10):
        """
        获取频道最新视频信息
        :param channel_url: YouTube频道URL
        :param limit: 需要获取的视频数量
        :return: 视频信息列表
        """
        videos_info = []
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 获取频道信息
                channel_info = ydl.extract_info(channel_url, download=False)
                
                # 获取视频列表
                if 'entries' in channel_info:
                    videos = list(channel_info['entries'])[:limit]
                    
                    for video in videos:
                        video_info = {
                            '标题': video.get('title', 'Unknown'),
                            '视频链接': f"https://www.youtube.com/watch?v={video.get('id')}",
                            '封面': video.get('thumbnails', [{}])[-1].get('url', ''),  # 获取最高质量的缩略图
                            '发布者': channel_info.get('uploader', 'Unknown'),  # 从频道信息获取
                            '观看次数': video.get('view_count', 0),
                            '时长(秒)': str(video.get('duration', 'Unknown')),
                            '上传时间': video.get('upload_date', 'Unknown')
                        }
                        videos_info.append(video_info)
        
        except Exception as e:
            print(f"获取视频时发生错误: {str(e)}")
        
        return videos_info

    def save_video_info(self, video_info):
        # 保存为HTML
        template_env = Environment(loader=FileSystemLoader('.'))
        template = template_env.get_template('template.html')
        html_content = template.render(videos=[video_info])
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 同时保存为JSON
        with open('youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump([video_info], f, ensure_ascii=False, indent=2)

def main():
    # 这里输入要爬取的YouTube频道URL
    channel_url = "https://www.youtube.com/@mkbhd/videos"  # 替换为你想爬取的频道URL
    
    try:
        # 创建爬虫实例
        crawler = YouTubeChannelCrawler()
        
        # 获取最新1个视频的信息
        print("正在获取最新视频信息...")
        videos = crawler.get_channel_videos(channel_url, 1)
        
        # 打印结果
        for i, video in enumerate(videos, 1):
            print(f"\n=== 视频 {i} ===")
            for key, value in video.items():
                if key == '观看次数':
                    print(f"{key}: {value:,}")
                else:
                    print(f"{key}: {value}")
        
        # 保存结果到JSON文件
        crawler.save_video_info(videos[0])
        print("\n结果已保存到 index.html 和 youtube_videos.json")
        
        # 提示用户如何查看结果
        print("\n你可以通过以下方式查看结果：")
        print("1. 运行 start_server.bat 启动web服务器")
        print("2. 在浏览器中访问 http://localhost:8000")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
