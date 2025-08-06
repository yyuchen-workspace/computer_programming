from flask import Flask, render_template, request, jsonify, session
import threading
import json
import os
from datetime import datetime
from scraper import CommunityDataScraper
from models import db, ScrapingJob, CommunityData, ScrapingLog, UserSettings
import uuid
import time
app = Flask(__name__)
app.secret_key = 'community_scraper_secret_key_2025'
# 資料庫配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化資料庫
db.init_app(app)
# 存儲爬取任務的全局字典
scraping_tasks = {}