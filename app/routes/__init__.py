"""
app/routes/__init__.py
註冊所有 Blueprint 到 Flask App。
"""


def register_blueprints(app):
    """註冊所有路由 Blueprint"""
    from .main import bp as main_bp
    from .transaction import bp as transaction_bp
    from .category import bp as category_bp
    from .analysis import bp as analysis_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(analysis_bp)
