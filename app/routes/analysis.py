"""
app/routes/analysis.py
分析報表模組路由

負責收支分析功能，包含：
- 圓餅圖分析（月度各類別收支佔比）
- 月度收支摘要（近 12 個月統計）
"""
from flask import Blueprint, render_template, request

bp = Blueprint('analysis', __name__)


@bp.route('/analysis')
def charts():
    """
    圓餅圖分析

    GET /analysis

    輸入（Query 參數，皆選填）：
    - year: 年份（整數，預設當年）
    - month: 月份（整數，預設當月）

    處理邏輯：
    1. 解析年月參數（無效則使用當年當月）
    2. 呼叫 Transaction.get_monthly_category_summary(year, month) 取得彙總資料
    3. 分離收入與支出資料

    輸出：渲染 analysis/charts.html
    傳入變數：income_data, expense_data, year, month

    錯誤處理：無效的年月 → 使用當年當月
    """
    # TODO: 實作圓餅圖分析邏輯
    pass


@bp.route('/analysis/summary')
def summary():
    """
    月度收支摘要

    GET /analysis/summary

    輸入：無

    處理邏輯：呼叫 Transaction.get_monthly_summary(months=12) 取得近 12 個月摘要

    輸出：渲染 analysis/summary.html
    傳入變數：monthly_data
    """
    # TODO: 實作月度摘要邏輯
    pass
