"""
app/__init__.py
Flask Application Factory
"""
import os
from flask import Flask
from config import config
from app.models import db


def create_app(config_name='default'):
    """Flask 應用工廠函式"""
    app = Flask(__name__)
    
    # 載入組態設定
    app.config.from_object(config[config_name])
    
    # 初始化擴充套件
    db.init_app(app)
    
    # 註冊 Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # 確保 instance 目錄存在
    os.makedirs(app.instance_path, exist_ok=True)
    
    return app
