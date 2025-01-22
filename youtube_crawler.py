import yt_dlp
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import subprocess
import os

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class YouTubeCrawler:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'no_warnings': True,
            'format': 'best'
        }

    def get_channel_videos(self, channel_url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # 获取频道信息
                result = ydl.extract_info(channel_url, download=False)
                if 'entries' in result and result['entries']:
                    # 获取第一个视频的信息
                    video = result['entries'][0]
                    
                    # 从URL中提取频道名称
                    channel_name = channel_url.split('@')[1].split('/')[0]
                    
                    # 获取最高质量的缩略图
                    thumbnail = ''
                    if 'thumbnails' in video and video['thumbnails']:
                        # 按质量排序缩略图
                        thumbnails = sorted(
                            video['thumbnails'], 
                            key=lambda x: (x.get('height', 0) * x.get('width', 0)), 
                            reverse=True
                        )
                        thumbnail = thumbnails[0].get('url', '') if thumbnails else ''
                    
                    # 构建视频数据
                    video_data = {
                        '标题': video.get('title', 'Unknown'),
                        '发布者': channel_name,
                        '观看次数': video.get('view_count', 0),
                        '时长(秒)': video.get('duration', 0),
                        '视频链接': f"https://www.youtube.com/watch?v={video.get('id')}",
                        '封面': thumbnail,
                        '抓取时间': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    return [video_data]
            return []
        except Exception as e:
            print(f"\n✗ {channel_url}: {str(e)}")
            return []

    def save_videos_info(self, videos_info):
        # 保存JSON文件
        with open('youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos_info, f, ensure_ascii=False, indent=2)
        
        # 生成HTML内容
        html_content = self.generate_html(videos_info)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def generate_html(self, videos):
        html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Latest Videos</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        .video-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .video-card:hover {
            transform: translateY(-5px);
        }
        .thumbnail {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .video-info {
            padding: 15px;
        }
        .video-title {
            font-size: 16px;
            font-weight: 600;
            margin: 0 0 10px 0;
            color: #333;
        }
        .video-meta {
            font-size: 14px;
            color: #666;
        }
        .update-time {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 14px;
        }
        a {
            text-decoration: none;
            color: inherit;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>YouTube Latest Videos</h1>
    </div>
    <div class="video-grid">
'''
        
        for video in videos:
            html += f'''
        <a href="{video['视频链接']}" target="_blank" class="video-card">
            <img src="{video['封面']}" alt="{video['标题']}" class="thumbnail">
            <div class="video-info">
                <h2 class="video-title">{video['标题']}</h2>
                <div class="video-meta">
                    <div>发布者: {video['发布者']}</div>
                    <div>观看次数: {video['观看次数']:,}</div>
                </div>
            </div>
        </a>'''

        html += f'''
    </div>
    <div class="update-time">
        最后更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
'''
        return html

def git_push_changes():
    try:
        # 检查是否有更改
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not status.stdout.strip():
            print("没有需要提交的更改")
            return False

        # 添加更改
        subprocess.run(['git', 'add', 'youtube_videos.json', 'index.html'], check=True)
        
        # 提交更改
        commit_message = f"Update videos: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # 推送到GitHub
        subprocess.run(['git', 'push'], check=True)
        
        print("✅ 成功推送更改到GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        return False

def main():
    # YouTube频道列表
    channels = [
        "https://www.youtube.com/@GregIsenberg/videos",
        "https://www.youtube.com/@Tan_Dongdong/videos",
        "https://www.youtube.com/@MoneyXYZ/videos",
        "https://www.youtube.com/@xiao_lin_shuo/videos",
        "https://www.youtube.com/@nicolevdh/videos",
        "https://www.youtube.com/@TheVerge/videos",
        "https://www.youtube.com/@mkbhd/videos",
        "https://www.youtube.com/@lexfridman/videos",
        "https://www.youtube.com/@AlexFinnOfficial/videos",
        "https://www.youtube.com/@huanyihe777/videos",
        "https://www.youtube.com/@mreflow/videos",
        "https://www.youtube.com/@linkingyourthinking/videos",
        "https://www.youtube.com/@hubermanlab/videos",
        "https://www.youtube.com/@casey/videos",
        "https://www.youtube.com/@JordanWelch/videos",
        "https://www.youtube.com/@TheMarketMemo/videos",
        "https://www.youtube.com/@marktilbury/videos",
        "https://www.youtube.com/@matthew_berman/videos",
        "https://www.youtube.com/@OurRichJourney/videos",
        "https://www.youtube.com/@timferriss/videos",
        "https://www.youtube.com/@WhatBitcoinDidPod/videos",
        "https://www.youtube.com/@ycombinator/videos",
        "https://www.youtube.com/@rileybrownai/videos",
        "https://www.youtube.com/@AIDiscovery2045/videos",
        "https://www.youtube.com/@realmckaywrigley/videos",
        "https://www.youtube.com/@AllAboutAI/videos",
        "https://www.youtube.com/@VoloBuilds/videos",
        "https://www.youtube.com/@VercelHQ/videos",
        "https://www.youtube.com/@rasmic/videos",
        "https://www.youtube.com/@ColeMedin/videos",
        "https://www.youtube.com/@GregIsenberg/videos",
        "https://www.youtube.com/@AIJasonZ/videos",
        "https://www.youtube.com/@AIGCLINK/videos",
        "https://www.youtube.com/@lifeofwayne/videos"
    ]
    
    start_time = time.time()
    crawler = YouTubeCrawler()
    all_videos = []
    
    print("开始获取视频信息...")
    
    # 增加并发数到10
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(crawler.get_channel_videos, url): url for url in channels}
        
        with tqdm(total=len(channels), desc="处理进度", ncols=100) as pbar:
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    videos = future.result()
                    if videos:
                        all_videos.extend(videos)
                        channel_name = videos[0]['发布者']
                        tqdm.write(f"✓ {channel_name}")
                except Exception as e:
                    tqdm.write(f"✗ 处理失败: {url}")
                pbar.update(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if all_videos:
        crawler.save_videos_info(all_videos)
        print(f"\n✅ 成功获取 {len(all_videos)} 个频道的视频信息")
        print(f"⏱️ 总用时: {duration:.2f} 秒")
        print("📝 结果已保存到 youtube_videos.json 和 index.html")
        
        # 推送到GitHub
        git_push_changes()
    else:
        print("\n❌ 没有获取到任何视频信息")

if __name__ == "__main__":
    main()
