import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import sys
from tqdm import tqdm
import random

# 设置控制台输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class TwitterCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # nitter实例列表
        self.instances = [
            'https://nitter.net',
            'https://nitter.cz',
            'https://nitter.1d4.us',
            'https://nitter.kavin.rocks',
            'https://nitter.unixfox.eu',
            'https://nitter.fdn.fr',
            'https://nitter.mint.lgbt',
            'https://nitter.moomoo.me',
            'https://nitter.privacydev.net',
            'https://nitter.poast.org'
        ]

    async def get_user_tweet(self, session, username):
        # 随机打乱实例列表
        instances = self.instances.copy()
        random.shuffle(instances)
        
        # 尝试每个实例
        for instance in instances:
            try:
                url = f'{instance}/{username}'
                async with session.get(url, headers=self.headers, ssl=False, timeout=3) as response:
                    if response.status != 200:
                        print(f"✗ {username}: HTTP {response.status} from {instance}")
                        continue

                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    tweet = soup.find('div', class_='tweet-content')
                    
                    if not tweet:
                        print(f"✗ {username}: No tweets found on {instance}")
                        continue

                    content = tweet.get_text(strip=True)
                    
                    tweet_data = {
                        '作者': username,
                        '内容': content,
                        '抓取时间': time.strftime('%Y-%m-%d %H:%M:%S'),
                        '来源': instance
                    }
                    
                    print(f"✓ {username}: {content[:50]}...")  # 只在打印时显示前50个字符，但保存完整内容
                    return tweet_data
                    
            except asyncio.TimeoutError:
                print(f"✗ {username}: Timeout on {instance}")
                continue
            except Exception as e:
                print(f"✗ {username}: Error on {instance} - {str(e)}")
                continue
        
        print(f"✗ {username}: Failed on all instances")
        return None

    async def get_all_tweets(self, users):
        # 设置更宽松的连接限制
        conn = aiohttp.TCPConnector(limit=10, force_close=True, enable_cleanup_closed=True)
        timeout = aiohttp.ClientTimeout(total=30, connect=3, sock_connect=3, sock_read=3)
        
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            tasks = []
            for username in users:
                task = asyncio.create_task(self.get_user_tweet(session, username))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return [r for r in results if r is not None]

    def save_tweets_info(self, tweets_info):
        # 保存JSON文件
        with open('twitter_posts.json', 'w', encoding='utf-8') as f:
            json.dump(tweets_info, f, ensure_ascii=False, indent=2)
        
        # 生成HTML内容
        html_content = self.generate_html(tweets_info)
        with open('twitter.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def generate_html(self, tweets):
        html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Latest Posts</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .tweet-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .tweet-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .tweet-content {
            font-size: 16px;
            margin: 0 0 10px 0;
            color: #333;
        }
        .tweet-meta {
            font-size: 14px;
            color: #666;
            display: flex;
            justify-content: space-between;
        }
        .update-time {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Twitter Latest Posts</h1>
    </div>
    <div class="tweet-list">
'''
        
        for tweet in tweets:
            html += f'''
        <div class="tweet-card">
            <div class="tweet-content">{tweet['内容']}</div>
            <div class="tweet-meta">
                <span>@{tweet['作者']}</span>
                <span>{tweet['抓取时间']}</span>
            </div>
        </div>'''

        html += f'''
    </div>
    <div class="update-time">
        最后更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
'''
        return html

async def main():
    # Twitter用户列表
    users = [
        "levelsio",      # Pieter Levels
        "AxtonLiu",      # Axton Liu
        "dotey",         # Dotey
        "mckaywrigley",  # McKay Wrigley
        "aigclink",      # AIGC Link
        "op7418"         # OP7418
    ]
    
    start_time = time.time()
    crawler = TwitterCrawler()
    
    print("开始获取推文信息...")
    
    # 禁用SSL验证警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 异步获取所有推文
    all_tweets = await crawler.get_all_tweets(users)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if all_tweets:
        crawler.save_tweets_info(all_tweets)
        print(f"\n✅ 成功获取 {len(all_tweets)} 条推文")
        print(f"⏱️ 总用时: {duration:.2f} 秒")
        print("📝 结果已保存到 twitter_posts.json 和 twitter.html")
    else:
        print("\n❌ 没有获取到任何推文")

if __name__ == "__main__":
    # Windows需要特别设置事件循环策略
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
