import pytest
from content import ContentRepository, Content

@pytest.fixture
def content_repo():
    return ContentRepository()

def test_load_content(content_repo):
    assert len(content_repo.content) > 0  # Ensure there is at least one content item

def test_get_content_by_page(content_repo):
    content = content_repo.get_content(1)
    assert content is not None
    assert content.title == "محتوای شماره 1"
