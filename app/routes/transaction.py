"""
app/routes/transaction.py
交易紀錄模組路由
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Transaction, Category

bp = Blueprint('transaction', __name__)

@bp.route('/transactions')
def list_transactions():
    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')
    type = request.args.get('type')
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')

    date_from = None
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    date_to = None
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if category_id:
        try:
            category_id = int(category_id)
        except ValueError:
            category_id = None

    transactions = Transaction.get_filtered(
        date_from=date_from,
        date_to=date_to,
        type=type,
        category_id=category_id,
        keyword=keyword
    )
    categories = Category.get_all()
    filters = {
        'date_from': date_from_str,
        'date_to': date_to_str,
        'type': type,
        'category_id': category_id,
        'keyword': keyword
    }
    
    return render_template('transactions/list.html', transactions=transactions, categories=categories, filters=filters)

@bp.route('/transactions/new', methods=['GET'])
def new_transaction():
    income_categories = Category.get_by_type('income')
    expense_categories = Category.get_by_type('expense')
    return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

@bp.route('/transactions/new', methods=['POST'])
def create_transaction():
    amount_str = request.form.get('amount')
    type = request.form.get('type')
    category_id_str = request.form.get('category_id')
    date_str = request.form.get('date')
    note = request.form.get('note', '')

    income_categories = Category.get_by_type('income')
    expense_categories = Category.get_by_type('expense')

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("金額必須大於 0")
    except (TypeError, ValueError):
        flash('金額必須大於 0', 'danger')
        return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

    if type not in ['income', 'expense']:
        flash('無效的交易類型', 'danger')
        return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

    try:
        category_id = int(category_id_str)
    except (TypeError, ValueError):
        flash('請選擇有效的類別', 'danger')
        return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        flash('請輸入正確的日期格式', 'danger')
        return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

    try:
        Transaction.create(amount=amount, type=type, category_id=category_id, date=date, note=note)
        flash('交易建立成功', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return render_template('transactions/form.html', income_categories=income_categories, expense_categories=expense_categories, transaction=None)

@bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    transaction = Transaction.get_by_id(id)
    income_categories = Category.get_by_type('income')
    expense_categories = Category.get_by_type('expense')
    return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

@bp.route('/transactions/<int:id>/edit', methods=['POST'])
def update_transaction(id):
    transaction = Transaction.get_by_id(id)
    amount_str = request.form.get('amount')
    type = request.form.get('type')
    category_id_str = request.form.get('category_id')
    date_str = request.form.get('date')
    note = request.form.get('note', '')

    income_categories = Category.get_by_type('income')
    expense_categories = Category.get_by_type('expense')

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("金額必須大於 0")
    except (TypeError, ValueError):
        flash('金額必須大於 0', 'danger')
        return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

    if type not in ['income', 'expense']:
        flash('無效的交易類型', 'danger')
        return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

    try:
        category_id = int(category_id_str)
    except (TypeError, ValueError):
        flash('請選擇有效的類別', 'danger')
        return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        flash('請輸入正確的日期格式', 'danger')
        return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

    try:
        transaction.update(amount=amount, type=type, category_id=category_id, date=date, note=note)
        flash('交易更新成功', 'success')
        return redirect(url_for('transaction.list_transactions'))
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return render_template('transactions/form.html', transaction=transaction, income_categories=income_categories, expense_categories=expense_categories)

@bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    transaction = Transaction.get_by_id(id)
    try:
        transaction.delete()
        flash('交易刪除成功', 'success')
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        
    return redirect(url_for('transaction.list_transactions'))
