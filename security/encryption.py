from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def get_key(self):
        return self.key

    def encrypt(self, plaintext):
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        return self.fernet.decrypt(ciphertext.encode()).decode()
