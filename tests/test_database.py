import pytest
import sqlite3
from src.database import DatabaseManager


@pytest.fixture
def db_manager():
    """مورد آزمایشی مدیریت پایگاه داده"""
    # ایجاد پایگاه داده موقت برای تست
    db_manager = DatabaseManager()
    yield db_manager
    # بعد از تست، پایگاه داده را بازنشانی می‌کنیم
    db_manager.cursor.execute("DROP TABLE IF EXISTS users")
    db_manager.cursor.execute("DROP TABLE IF EXISTS favorites")
    db_manager.conn.commit()


def test_get_user_page(db_manager):
    """تست برای گرفتن صفحه کاربر"""
    user_id = 123
    db_manager.get_user_page(user_id)
    db_manager.cursor.execute("SELECT page FROM users WHERE id = ?", (user_id,))
    page = db_manager.cursor.fetchone()[0]
    assert page == 1  # باید صفحه ۱ را برگرداند


def test_add_favorite(db_manager):
    """تست برای اضافه کردن علاقه‌مندی"""
    user_id = 123
    page = 2
    db_manager.add_favorite(user_id, page)
    db_manager.cursor.execute("SELECT page FROM favorites WHERE user_id = ? AND page = ?", (user_id, page))
    result = db_manager.cursor.fetchone()
    assert result is not None  # باید رکورد اضافه شده باشد
