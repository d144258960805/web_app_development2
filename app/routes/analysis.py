"""
app/routes/analysis.py
分析報表模組路由
"""
from datetime import datetime
from flask import Blueprint, render_template, request
from app.models import Transaction

bp = Blueprint('analysis', __name__)

@bp.route('/analysis')
def charts():
    year_str = request.args.get('year')
    month_str = request.args.get('month')
    
    now = datetime.now()
    try:
        year = int(year_str) if year_str else now.year
        month = int(month_str) if month_str else now.month
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        year = now.year
        month = now.month

    summary_data = Transaction.get_monthly_category_summary(year, month)
    
    income_data = [d for d in summary_data if d['type'] == 'income']
    expense_data = [d for d in summary_data if d['type'] == 'expense']
    
    return render_template('analysis/charts.html', income_data=income_data, expense_data=expense_data, year=year, month=month)

@bp.route('/analysis/summary')
def summary():
    monthly_data = Transaction.get_monthly_summary(months=12)
    return render_template('analysis/summary.html', monthly_data=monthly_data)
