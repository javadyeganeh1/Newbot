import sqlite3
from typing import List

class DatabaseManager:
    """Class for managing database operations"""

    def __init__(self):
        self.conn = sqlite3.connect("bot_data.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables in the database"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                page INTEGER DEFAULT 1
            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                page INTEGER,
                PRIMARY KEY (user_id, page)
            )"""
        )
        self.conn.commit()

    def get_user_page(self, user_id: int) -> int:
        """Get the current page of a user"""
        self.cursor.execute(
            "SELECT page FROM users WHERE id = ?", (user_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]
        self.cursor.execute(
            "INSERT INTO users (id, page) VALUES (?, 1)", (user_id,)
        )
        self.conn.commit()
        return 1

    def set_user_page(self, user_id: int, page: int):
        """Set the current page for a user"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO users (id, page) VALUES (?, ?)",
            (user_id, page),
        )
        self.conn.commit()

    def add_favorite(self, user_id: int, page: int):
        """Add a page to user's favorites"""
        self.cursor.execute(
            "INSERT OR IGNORE INTO favorites (user_id, page) VALUES (?, ?)",
            (user_id, page),
        )
        self.conn.commit()

    def remove_favorite(self, user_id: int, page: int):
        """Remove a page from user's favorites"""
        self.cursor.execute(
            "DELETE FROM favorites WHERE user_id = ? AND page = ?",
            (user_id, page),
        )
        self.conn.commit()

    def get_favorites(self, user_id: int) -> List[int]:
        """Get all favorite pages for a user"""
        self.cursor.execute(
            "SELECT page FROM favorites WHERE user_id = ?", (user_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]
