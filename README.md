# YouTube Video Viewer

这是一个自动抓取YouTube视频信息的工具，使用GitHub Pages展示结果。

## 功能特点

- 自动抓取指定YouTube频道的最新视频信息
- 显示视频标题、缩略图、观看次数等信息
- 每6小时自动更新一次
- 移动端友好的响应式设计

## 使用方法

1. 访问 https://[你的用户名].github.io/[仓库名] 查看最新视频信息
2. 点击视频卡片上的"观看视频"按钮跳转到YouTube观看完整视频

## 本地开发

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行爬虫：`python youtube_crawler.py`
4. 在浏览器中打开 `index.html`
