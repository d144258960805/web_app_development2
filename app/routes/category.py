"""
app/routes/category.py
類別管理模組路由

負責收支類別的 CRUD 操作，包含：
- 類別列表
- 新增類別
- 編輯類別
- 刪除類別
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('category', __name__)


@bp.route('/categories')
def list_categories():
    """
    類別列表

    GET /categories

    處理邏輯：呼叫 Category.get_all() 取得所有類別

    輸出：渲染 categories/list.html
    傳入變數：categories
    """
    # TODO: 實作類別列表邏輯
    pass


@bp.route('/categories/new', methods=['GET'])
def new_category():
    """
    新增類別頁面

    GET /categories/new

    處理邏輯：無

    輸出：渲染 categories/form.html
    傳入變數：category=None（新增模式）
    """
    # TODO: 實作新增類別頁面邏輯
    pass


@bp.route('/categories/new', methods=['POST'])
def create_category():
    """
    建立類別

    POST /categories/new

    輸入（表單欄位）：
    - name: 類別名稱（必填，最多 50 字元）
    - type: 類別類型（必填，income / expense）

    處理邏輯：
    1. 驗證表單資料
    2. 檢查同類型下是否有重複名稱
    3. 呼叫 Category.create(...) 建立類別

    輸出：
    - 成功 → 重導向 /categories
    - 失敗 → 重新渲染 categories/form.html 並顯示錯誤

    錯誤處理：
    - 名稱為空 → 顯示「請輸入類別名稱」
    - 名稱重複 → 顯示「此類別名稱已存在」
    """
    # TODO: 實作建立類別邏輯
    pass


@bp.route('/categories/<int:id>/edit', methods=['GET'])
def edit_category(id):
    """
    編輯類別頁面

    GET /categories/<id>/edit

    輸入：URL 參數 id（整數）

    處理邏輯：呼叫 Category.get_by_id(id) 取得類別

    輸出：渲染 categories/form.html
    傳入變數：category（現有資料）

    錯誤處理：ID 不存在 → 404 Not Found
    """
    # TODO: 實作編輯類別頁面邏輯
    pass


@bp.route('/categories/<int:id>/edit', methods=['POST'])
def update_category(id):
    """
    更新類別

    POST /categories/<id>/edit

    輸入：URL 參數 id + 表單欄位（同建立類別）

    處理邏輯：
    1. 取得類別
    2. 驗證資料
    3. 呼叫 category.update(...) 更新

    輸出：
    - 成功 → 重導向 /categories
    - 失敗 → 重新渲染 categories/form.html

    錯誤處理：同建立類別 + ID 不存在 → 404
    """
    # TODO: 實作更新類別邏輯
    pass


@bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    刪除類別

    POST /categories/<id>/delete

    輸入：URL 參數 id（整數）

    處理邏輯：
    1. 取得類別
    2. 檢查是否有關聯的交易紀錄
    3. 呼叫 category.delete() 刪除

    輸出：重導向 /categories

    錯誤處理：
    - ID 不存在 → 404 Not Found
    - 有關聯交易 → 顯示提示「此類別下仍有交易紀錄，請先刪除相關交易」
    """
    # TODO: 實作刪除類別邏輯
    pass
