import pytest
from src.content import ContentRepository, Content

@pytest.fixture
def content_repo():
    """ایجاد نمونه‌ای از ContentRepository برای تست"""
    repo = ContentRepository()
    repo.content = [
        Content("عنوان ۱", "متن ۱"),
        Content("عنوان ۲", "متن ۲"),
    ]
    repo.total_pages = len(repo.content)
    return repo

def test_load_content(content_repo):
    """بررسی بارگذاری محتوا"""
    assert len(content_repo.content) == 2  # بررسی تعداد محتواها
    assert content_repo.content[0].title == "عنوان ۱"  # بررسی عنوان اولین محتوا

def test_get_content(content_repo):
    """بررسی دریافت محتوا بر اساس شماره صفحه"""
    content = content_repo.get_content(1)
    assert content is not None
    assert content.title == "عنوان ۱"
    assert content.text == "متن ۱"

    content = content_repo.get_content(3)  # صفحه‌ای که وجود ندارد
    assert content is None
