"""
app/models/category.py
收支類別模型（Category）

對應資料表：categories
關聯：一個 Category 可擁有多筆 Transaction（一對多）
"""
from datetime import datetime
from . import db


class Category(db.Model):
    """收支類別模型"""
    __tablename__ = 'categories'

    # --------------------------------------------------
    # 欄位定義
    # --------------------------------------------------
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='類別名稱')
    type = db.Column(
        db.String(10),
        nullable=False,
        comment='類別類型：income / expense'
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment='建立時間'
    )

    # --------------------------------------------------
    # 關聯
    # --------------------------------------------------
    # 一個類別擁有多筆交易（反向關聯）
    transactions = db.relationship(
        'Transaction',
        backref='category',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # --------------------------------------------------
    # 約束
    # --------------------------------------------------
    __table_args__ = (
        db.UniqueConstraint('name', 'type', name='uq_category_name_type'),
        db.CheckConstraint("type IN ('income', 'expense')", name='ck_category_type'),
    )

    # --------------------------------------------------
    # CRUD 方法
    # --------------------------------------------------
    @classmethod
    def create(cls, name, type):
        """建立新類別"""
        category = cls(name=name, type=type)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_all(cls):
        """取得所有類別"""
        return cls.query.order_by(cls.type, cls.name).all()

    @classmethod
    def get_by_id(cls, category_id):
        """依 ID 取得單一類別"""
        return cls.query.get_or_404(category_id)

    @classmethod
    def get_by_type(cls, type):
        """依類型取得類別列表（income / expense）"""
        return cls.query.filter_by(type=type).order_by(cls.name).all()

    def update(self, name=None, type=None):
        """更新類別資料"""
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        db.session.commit()
        return self

    def delete(self):
        """刪除類別（若有關聯交易會一併刪除）"""
        db.session.delete(self)
        db.session.commit()

    # --------------------------------------------------
    # 輔助方法
    # --------------------------------------------------
    @classmethod
    def seed_defaults(cls):
        """初始化預設類別（若不存在才建立）"""
        defaults = [
            # 支出類別
            ('餐飲', 'expense'),
            ('交通', 'expense'),
            ('娛樂', 'expense'),
            ('購物', 'expense'),
            ('住宿', 'expense'),
            ('醫療', 'expense'),
            ('教育', 'expense'),
            ('其他支出', 'expense'),
            # 收入類別
            ('薪水', 'income'),
            ('獎學金', 'income'),
            ('打工', 'income'),
            ('零用錢', 'income'),
            ('投資', 'income'),
            ('其他收入', 'income'),
        ]
        for name, type in defaults:
            existing = cls.query.filter_by(name=name, type=type).first()
            if not existing:
                db.session.add(cls(name=name, type=type))
        db.session.commit()

    def __repr__(self):
        return f'<Category {self.id}: {self.name} ({self.type})>'
