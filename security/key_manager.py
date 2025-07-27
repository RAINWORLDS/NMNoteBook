class KeyManager:
    @staticmethod
    def save_key(path, key):
        with open(path, "wb") as f:
            f.write(key)

    @staticmethod
    def load_key(path):
        with open(path, "rb") as f:
            return f.read()
