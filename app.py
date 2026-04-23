"""
app.py
Application Entry Point
"""
import os
from app import create_app
from app.models import db, Category

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.cli.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    Category.seed_defaults()
    print("Initialized the database with seed data.")

if __name__ == '__main__':
    app.run(debug=True)
