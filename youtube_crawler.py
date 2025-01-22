import yt_dlp
import json
from datetime import datetime
import sys
import webbrowser
from jinja2 import Environment, FileSystemLoader

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class YouTubeCrawler:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
            'no_warnings': True
        }

    def get_channel_videos(self, channel_url):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                result = ydl.extract_info(channel_url, download=False)
                if 'entries' in result:
                    videos_info = []
                    for entry in result['entries'][:1]:  # 只获取最新的一个视频
                        try:
                            video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                            video_info = ydl.extract_info(video_url, download=False)
                            
                            video_data = {
                                '标题': video_info.get('title', 'Unknown'),
                                '发布者': video_info.get('uploader', 'Unknown'),
                                '观看次数': video_info.get('view_count', 0),
                                '时长(秒)': video_info.get('duration', 0),
                                '视频链接': video_url,
                                '封面': video_info.get('thumbnail', '')
                            }
                            videos_info.append(video_data)
                            print(f"成功获取视频信息: {video_data['标题']}")
                        except Exception as e:
                            print(f"获取视频详细信息时出错: {str(e)}")
                    return videos_info
                return []
            except Exception as e:
                print(f"获取频道信息时出错: {str(e)}")
                return []

    def save_videos_info(self, videos_info):
        # 保存为JSON
        with open('youtube_videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos_info, f, ensure_ascii=False, indent=2)

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
    
    crawler = YouTubeCrawler()
    all_videos = []
    
    print("开始获取视频信息...")
    for channel_url in channels:
        print(f"\n正在处理频道: {channel_url}")
        videos = crawler.get_channel_videos(channel_url)
        if videos:
            all_videos.extend(videos)
    
    if all_videos:
        # 保存所有视频信息
        crawler.save_videos_info(all_videos)
        print(f"\n成功获取 {len(all_videos)} 个频道的视频信息")
        print("结果已保存到 youtube_videos.json")
    else:
        print("\n没有获取到任何视频信息")

if __name__ == "__main__":
    main()
