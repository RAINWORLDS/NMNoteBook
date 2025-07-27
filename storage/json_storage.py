import json
import os

class JSONStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        # 确保文件存在
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
