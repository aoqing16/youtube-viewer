from flask import Flask, render_template, jsonify, send_from_directory
import json
import os
import logging
from logging.handlers import RotatingFileHandler

# 设置日志
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

app = Flask(__name__)

# 配置日志
handler = RotatingFileHandler(
    os.path.join(log_dir, 'server.log'),
    maxBytes=10000000,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    app.logger.info('访问主页')
    return send_from_directory('.', 'viewer.html')

@app.route('/youtube_videos.json')
def get_videos():
    try:
        with open('youtube_videos.json', 'r', encoding='utf-8') as f:
            app.logger.info('成功读取视频数据')
            return jsonify(json.load(f))
    except FileNotFoundError:
        app.logger.error('未找到视频数据文件')
        return jsonify([])
    except Exception as e:
        app.logger.error(f'读取视频数据时出错: {str(e)}')
        return jsonify([])

if __name__ == '__main__':
    app.logger.info('服务器启动')
    app.run(host='0.0.0.0', port=8000, threaded=True)
