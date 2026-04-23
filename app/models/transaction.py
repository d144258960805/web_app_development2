"""
app/models/transaction.py
交易紀錄模型（Transaction）

對應資料表：transactions
關聯：每筆 Transaction 屬於一個 Category（多對一）
"""
from datetime import datetime, date
from sqlalchemy import func
from . import db


class Transaction(db.Model):
    """交易紀錄模型"""
    __tablename__ = 'transactions'

    # --------------------------------------------------
    # 欄位定義
    # --------------------------------------------------
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False, comment='交易金額（正數）')
    type = db.Column(
        db.String(10),
        nullable=False,
        comment='交易類型：income / expense'
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False,
        comment='關聯類別 ID'
    )
    date = db.Column(db.Date, nullable=False, comment='交易日期')
    note = db.Column(db.Text, nullable=False, default='', comment='備註')
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment='建立時間'
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment='最後更新時間'
    )

    # --------------------------------------------------
    # 約束與索引
    # --------------------------------------------------
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='ck_transaction_amount_positive'),
        db.CheckConstraint("type IN ('income', 'expense')", name='ck_transaction_type'),
        db.Index('idx_transactions_date', 'date'),
        db.Index('idx_transactions_type', 'type'),
        db.Index('idx_transactions_category_id', 'category_id'),
    )

    # --------------------------------------------------
    # 關聯（backref 已在 Category 模型中定義）
    # --------------------------------------------------
    # 可透過 self.category 存取所屬類別

    # --------------------------------------------------
    # CRUD 方法
    # --------------------------------------------------
    @classmethod
    def create(cls, amount, type, category_id, date, note=''):
        """建立新交易紀錄"""
        transaction = cls(
            amount=amount,
            type=type,
            category_id=category_id,
            date=date,
            note=note
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @classmethod
    def get_all(cls, order_by_date_desc=True):
        """取得所有交易紀錄"""
        query = cls.query
        if order_by_date_desc:
            query = query.order_by(cls.date.desc(), cls.created_at.desc())
        return query.all()

    @classmethod
    def get_by_id(cls, transaction_id):
        """依 ID 取得單一交易紀錄"""
        return cls.query.get_or_404(transaction_id)

    def update(self, amount=None, type=None, category_id=None, date=None, note=None):
        """更新交易紀錄"""
        if amount is not None:
            self.amount = amount
        if type is not None:
            self.type = type
        if category_id is not None:
            self.category_id = category_id
        if date is not None:
            self.date = date
        if note is not None:
            self.note = note
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    def delete(self):
        """刪除交易紀錄"""
        db.session.delete(self)
        db.session.commit()

    # --------------------------------------------------
    # 查詢方法
    # --------------------------------------------------
    @classmethod
    def get_filtered(cls, date_from=None, date_to=None, type=None,
                     category_id=None, keyword=None):
        """
        依條件篩選交易紀錄

        Args:
            date_from: 起始日期（含）
            date_to: 結束日期（含）
            type: 交易類型（income / expense）
            category_id: 類別 ID
            keyword: 備註關鍵字
        """
        query = cls.query

        if date_from:
            query = query.filter(cls.date >= date_from)
        if date_to:
            query = query.filter(cls.date <= date_to)
        if type:
            query = query.filter(cls.type == type)
        if category_id:
            query = query.filter(cls.category_id == category_id)
        if keyword:
            query = query.filter(cls.note.ilike(f'%{keyword}%'))

        return query.order_by(cls.date.desc(), cls.created_at.desc()).all()

    @classmethod
    def get_recent(cls, limit=10):
        """取得最近的交易紀錄"""
        return cls.query.order_by(
            cls.date.desc(), cls.created_at.desc()
        ).limit(limit).all()

    # --------------------------------------------------
    # 統計方法
    # --------------------------------------------------
    @classmethod
    def get_balance_summary(cls):
        """
        計算總餘額統計

        Returns:
            dict: {
                'total_income': 總收入,
                'total_expense': 總支出,
                'balance': 餘額
            }
        """
        result = db.session.query(
            func.coalesce(
                func.sum(db.case(
                    (cls.type == 'income', cls.amount),
                    else_=0
                )), 0
            ).label('total_income'),
            func.coalesce(
                func.sum(db.case(
                    (cls.type == 'expense', cls.amount),
                    else_=0
                )), 0
            ).label('total_expense'),
        ).first()

        total_income = float(result.total_income)
        total_expense = float(result.total_expense)

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense
        }

    @classmethod
    def get_monthly_category_summary(cls, year, month):
        """
        取得指定月份各類別的收支彙總（圓餅圖用）

        Args:
            year: 年份（int）
            month: 月份（int）

        Returns:
            list of dict: [{'category_name': str, 'type': str, 'total': float}]
        """
        from .category import Category

        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)

        results = db.session.query(
            Category.name.label('category_name'),
            cls.type,
            func.sum(cls.amount).label('total')
        ).join(Category).filter(
            cls.date >= first_day,
            cls.date < last_day
        ).group_by(Category.id, cls.type).order_by(
            func.sum(cls.amount).desc()
        ).all()

        return [
            {
                'category_name': r.category_name,
                'type': r.type,
                'total': float(r.total)
            }
            for r in results
        ]

    @classmethod
    def get_monthly_summary(cls, months=12):
        """
        取得近 N 個月的收支摘要

        Args:
            months: 要取得的月份數量（預設 12）

        Returns:
            list of dict: [{
                'month': 'YYYY-MM',
                'total_income': float,
                'total_expense': float,
                'balance': float
            }]
        """
        results = db.session.query(
            func.strftime('%Y-%m', cls.date).label('month'),
            func.coalesce(
                func.sum(db.case(
                    (cls.type == 'income', cls.amount),
                    else_=0
                )), 0
            ).label('total_income'),
            func.coalesce(
                func.sum(db.case(
                    (cls.type == 'expense', cls.amount),
                    else_=0
                )), 0
            ).label('total_expense'),
        ).group_by(
            func.strftime('%Y-%m', cls.date)
        ).order_by(
            func.strftime('%Y-%m', cls.date).desc()
        ).limit(months).all()

        return [
            {
                'month': r.month,
                'total_income': float(r.total_income),
                'total_expense': float(r.total_expense),
                'balance': float(r.total_income) - float(r.total_expense)
            }
            for r in results
        ]

    # --------------------------------------------------
    # 表示方法
    # --------------------------------------------------
    def __repr__(self):
        return (
            f'<Transaction {self.id}: {self.type} '
            f'${self.amount:.2f} on {self.date}>'
        )
