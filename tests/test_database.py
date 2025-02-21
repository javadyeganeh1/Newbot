import pytest
from database import DatabaseManager

@pytest.fixture
def db():
    db = DatabaseManager()
    yield db
    # Clean up: after each test, you might want to reset the database
    db.cursor.execute("DELETE FROM users")
    db.cursor.execute("DELETE FROM favorites")
    db.conn.commit()

def test_add_and_get_user_page(db):
    db.set_user_page(1, 2)
    assert db.get_user_page(1) == 2

def test_add_and_remove_favorite(db):
    db.add_favorite(1, 1)
    assert 1 in db.get_favorites(1)
    
    db.remove_favorite(1, 1)
    assert 1 not in db.get_favorites(1)
