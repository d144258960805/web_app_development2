"""
app/models/__init__.py
匯出所有模型與資料庫實例，供其他模組使用。
"""
from flask_sqlalchemy import SQLAlchemy

# 建立 SQLAlchemy 實例（在 create_app 中初始化）
db = SQLAlchemy()

from .category import Category
from .transaction import Transaction

__all__ = ['db', 'Category', 'Transaction']
