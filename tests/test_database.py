import pytest
import sqlite3
from src.database import DatabaseManager

@pytest.fixture
def db():
    """ایجاد یک پایگاه داده موقتی برای تست"""
    db = DatabaseManager()
    db.conn = sqlite3.connect(":memory:")  # استفاده از دیتابیس در حافظه
    db.cursor = db.conn.cursor()
    db._create_tables()
    return db

def test_get_user_page(db):
    """بررسی مقدار پیش‌فرض صفحه کاربر"""
    user_id = 1
    assert db.get_user_page(user_id) == 1  # مقدار پیش‌فرض باید ۱ باشد

def test_set_user_page(db):
    """بررسی تنظیم شماره صفحه برای کاربر"""
    user_id = 1
    db.set_user_page(user_id, 3)
    assert db.get_user_page(user_id) == 3

def test_add_favorite(db):
    """بررسی افزودن به علاقه‌مندی‌ها"""
    user_id = 1
    page = 2
    db.add_favorite(user_id, page)
    assert db.get_favorites(user_id) == [2]

def test_remove_favorite(db):
    """بررسی حذف از علاقه‌مندی‌ها"""
    user_id = 1
    page = 2
    db.add_favorite(user_id, page)
    db.remove_favorite(user_id, page)
    assert db.get_favorites(user_id) == []
