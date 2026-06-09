from cryptography.fernet import Fernet
import os

class CryptoManager:
    def __init__(self):
        # Используем простой ключ для примера,
        # в реальном мессенджере ключи нужно хранить в БД для каждого юзера
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.encode()).decode()

def generate_user_keys():
    # Эта функция просто возвращает ключ в виде строки
    return Fernet.generate_key().decode()
