import json
from typing import List, Optional

class Content:
    """Represents a single content page"""
    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text

class ContentRepository:
    """Manages the collection of content pages"""
    def __init__(self):
        self.content = self._load_content()
        self.total_pages = len(self.content)

    def _load_content(self) -> List[Content]:
        """Load content from a JSON file"""
        with open("data/data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Content(title=item["title"], text=item["text"]) for item in data]

    def get_content(self, page: int) -> Optional[Content]:
        """Get content by page number"""
        if 1 <= page <= self.total_pages:
            return self.content[page - 1]
        return None
