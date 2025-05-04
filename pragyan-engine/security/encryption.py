from cryptography.fernet import Fernet


class Encryptor:
    def __init__(self, key: str):
        if not key:
            raise ValueError("Key cannot be none. Provide a valid key for encryption")
        self.fernet = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
