import pytest
from src.content import ContentRepository


@pytest.fixture
def content_repo():
    """مورد آزمایشی مخزن محتوا"""
    return ContentRepository()


def test_load_content(content_repo):
    """تست برای بارگذاری محتواها از فایل JSON"""
    assert len(content_repo.content) > 0  # باید حداقل یک محتوا وجود داشته باشد


def test_get_content(content_repo):
    """تست برای دریافت محتوا براساس شماره صفحه"""
    content = content_repo.get_content(1)
    assert content is not None
    assert content.title == "محتوای شماره 1"  # باید عنوان محتوا صحیح باشد
