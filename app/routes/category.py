"""
app/routes/category.py
類別管理模組路由
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlalchemy
from app.models import Category

bp = Blueprint('category', __name__)

@bp.route('/categories')
def list_categories():
    categories = Category.get_all()
    return render_template('categories/list.html', categories=categories)

@bp.route('/categories/new', methods=['GET'])
def new_category():
    return render_template('categories/form.html', category=None)

@bp.route('/categories/new', methods=['POST'])
def create_category():
    name = request.form.get('name', '').strip()
    type = request.form.get('type')

    if not name:
        flash('請輸入類別名稱', 'danger')
        return render_template('categories/form.html', category=None)
    
    if type not in ['income', 'expense']:
        flash('無效的類別類型', 'danger')
        return render_template('categories/form.html', category=None)

    try:
        Category.create(name=name, type=type)
        flash('類別建立成功', 'success')
        return redirect(url_for('category.list_categories'))
    except sqlalchemy.exc.IntegrityError:
        flash('此類別名稱已存在', 'danger')
        return render_template('categories/form.html', category=None)
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return render_template('categories/form.html', category=None)

@bp.route('/categories/<int:id>/edit', methods=['GET'])
def edit_category(id):
    category = Category.get_by_id(id)
    return render_template('categories/form.html', category=category)

@bp.route('/categories/<int:id>/edit', methods=['POST'])
def update_category(id):
    category = Category.get_by_id(id)
    name = request.form.get('name', '').strip()
    type = request.form.get('type')

    if not name:
        flash('請輸入類別名稱', 'danger')
        return render_template('categories/form.html', category=category)
    
    if type not in ['income', 'expense']:
        flash('無效的類別類型', 'danger')
        return render_template('categories/form.html', category=category)

    try:
        category.update(name=name, type=type)
        flash('類別更新成功', 'success')
        return redirect(url_for('category.list_categories'))
    except sqlalchemy.exc.IntegrityError:
        flash('此類別名稱已存在', 'danger')
        return render_template('categories/form.html', category=category)
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        return render_template('categories/form.html', category=category)

@bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    category = Category.get_by_id(id)
    if category.transactions:
        flash('此類別下仍有交易紀錄，請先刪除相關交易', 'danger')
        return redirect(url_for('category.list_categories'))
    
    try:
        category.delete()
        flash('類別刪除成功', 'success')
    except Exception as e:
        flash(f'發生錯誤: {str(e)}', 'danger')
        
    return redirect(url_for('category.list_categories'))
