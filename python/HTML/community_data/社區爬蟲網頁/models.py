#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Models for Community Scraper
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ScrapingJob(db.Model):
    """爬取任務記錄"""
    __tablename__ = 'scraping_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(36), unique=True, nullable=False, index=True)
    city_name = db.Column(db.String(50), nullable=False)
    subdivision = db.Column(db.String(10), nullable=False)  # "是" or "否"
    district_name = db.Column(db.String(50), nullable=True)
    all_districts = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='準備中')  # 準備中, 進行中, 完成, 失敗, 停止
    progress = db.Column(db.Integer, default=0)
    total_records = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # 關聯到社區資料
    communities = db.relationship('CommunityData', backref='scraping_job', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'city_name': self.city_name,
            'subdivision': self.subdivision,
            'district_name': self.district_name,
            'all_districts': self.all_districts,
            'status': self.status,
            'progress': self.progress,
            'total_records': self.total_records,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'error_message': self.error_message
        }

class CommunityData(db.Model):
    """社區資料"""
    __tablename__ = 'community_data'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'district': self.district,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ScrapingLog(db.Model):
    """爬取日誌"""
    __tablename__ = 'scraping_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(10), default='INFO')  # INFO, WARNING, ERROR
    message = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'message': self.message
        }

class UserSettings(db.Model):
    """使用者設定"""
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(50), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_setting(key, default=None):
        setting = UserSettings.query.filter_by(setting_key=key).first()
        if setting:
            try:
                return json.loads(setting.setting_value)
            except:
                return setting.setting_value
        return default
    
    @staticmethod
    def set_setting(key, value):
        setting = UserSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            setting.updated_at = datetime.utcnow()
        else:
            setting = UserSettings(
                setting_key=key,
                setting_value=json.dumps(value) if isinstance(value, (dict, list)) else str(value)
            )
            db.session.add(setting)
        db.session.commit()
        return setting