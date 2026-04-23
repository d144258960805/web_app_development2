"""
app/routes/transaction.py
交易紀錄模組路由

負責交易紀錄的 CRUD 操作，包含：
- 交易列表（含篩選搜尋）
- 新增交易
- 編輯交易
- 刪除交易
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('transaction', __name__)


@bp.route('/transactions')
def list_transactions():
    """
    交易列表

    GET /transactions

    輸入（Query 參數，皆選填）：
    - date_from: 起始日期（YYYY-MM-DD）
    - date_to: 結束日期（YYYY-MM-DD）
    - type: 交易類型（income / expense）
    - category_id: 類別 ID（整數）
    - keyword: 備註關鍵字

    處理邏輯：
    1. 解析篩選條件
    2. 呼叫 Transaction.get_filtered(...) 取得篩選結果
    3. 呼叫 Category.get_all() 取得類別列表（供篩選下拉選單）

    輸出：渲染 transactions/list.html
    傳入變數：transactions, categories, filters
    """
    # TODO: 實作交易列表邏輯
    pass


@bp.route('/transactions/new', methods=['GET'])
def new_transaction():
    """
    新增交易頁面

    GET /transactions/new

    處理邏輯：
    1. 呼叫 Category.get_by_type('income') 取得收入類別
    2. 呼叫 Category.get_by_type('expense') 取得支出類別

    輸出：渲染 transactions/form.html
    傳入變數：income_categories, expense_categories, transaction=None
    """
    # TODO: 實作新增交易頁面邏輯
    pass


@bp.route('/transactions/new', methods=['POST'])
def create_transaction():
    """
    建立交易

    POST /transactions/new

    輸入（表單欄位）：
    - amount: 金額（必填，正數）
    - type: 類型（必填，income / expense）
    - category_id: 類別 ID（必填，整數）
    - date: 日期（必填，YYYY-MM-DD）
    - note: 備註（選填）

    處理邏輯：
    1. 驗證表單資料（金額 > 0、類型合法、日期格式正確）
    2. 呼叫 Transaction.create(...) 建立紀錄

    輸出：
    - 成功 → 重導向 /
    - 失敗 → 重新渲染 transactions/form.html 並顯示錯誤

    錯誤處理：
    - 金額非正數 → 顯示「金額必須大於 0」
    - 類別不存在 → 顯示「請選擇有效的類別」
    - 日期格式錯誤 → 顯示「請輸入正確的日期格式」
    """
    # TODO: 實作建立交易邏輯
    pass


@bp.route('/transactions/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    編輯交易頁面

    GET /transactions/<id>/edit

    輸入：URL 參數 id（整數）

    處理邏輯：
    1. 呼叫 Transaction.get_by_id(id) 取得交易紀錄
    2. 取得所有類別供下拉選單

    輸出：渲染 transactions/form.html
    傳入變數：transaction（現有資料）, income_categories, expense_categories

    錯誤處理：ID 不存在 → 404 Not Found
    """
    # TODO: 實作編輯交易頁面邏輯
    pass


@bp.route('/transactions/<int:id>/edit', methods=['POST'])
def update_transaction(id):
    """
    更新交易

    POST /transactions/<id>/edit

    輸入：URL 參數 id + 表單欄位（同建立交易）

    處理邏輯：
    1. 呼叫 Transaction.get_by_id(id) 取得紀錄
    2. 驗證表單資料
    3. 呼叫 transaction.update(...) 更新紀錄

    輸出：
    - 成功 → 重導向 /transactions
    - 失敗 → 重新渲染 transactions/form.html

    錯誤處理：同建立交易 + ID 不存在 → 404
    """
    # TODO: 實作更新交易邏輯
    pass


@bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    刪除交易

    POST /transactions/<id>/delete

    輸入：URL 參數 id（整數）

    處理邏輯：
    1. 呼叫 Transaction.get_by_id(id) 取得紀錄
    2. 呼叫 transaction.delete() 刪除紀錄

    輸出：重導向 /transactions

    錯誤處理：ID 不存在 → 404 Not Found
    """
    # TODO: 實作刪除交易邏輯
    pass
