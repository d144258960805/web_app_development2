"""
app/routes/main.py
首頁模組路由

負責首頁總覽頁面，顯示餘額統計與近期交易紀錄。
"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    首頁總覽

    GET /

    處理邏輯：
    1. 呼叫 Transaction.get_balance_summary() 取得餘額統計
    2. 呼叫 Transaction.get_recent(limit=10) 取得近期交易

    輸出：渲染 index.html
    傳入變數：summary, recent_transactions
    """
    # TODO: 實作首頁邏輯
    pass
