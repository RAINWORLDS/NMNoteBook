import uuid
from datetime import datetime

class Note:
    def __init__(self, title, content, encrypted=False, timestamp=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.encrypted = encrypted
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "encrypted": self.encrypted,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            content=data["content"],
            encrypted=data.get("encrypted", False),
            timestamp=data.get("timestamp"),
            id=data.get("id"),
        )
