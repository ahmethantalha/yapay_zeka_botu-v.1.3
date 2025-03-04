from cryptography.fernet import Fernet
from src.core.exceptions import SecurityError
import base64
import os
import hashlib

class Security:
    """Handle encryption and decryption of sensitive data"""
    
    def __init__(self):
        self._key = os.getenv('ENCRYPTION_KEY')
        if not self._key:
            self._key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = self._key.decode()
        
        self._fernet = Fernet(self._key if isinstance(self._key, bytes) else self._key.encode())
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self._fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self._fernet.decrypt(encrypted_data.encode()).decode()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()