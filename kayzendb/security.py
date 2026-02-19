import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class SecurityManager:
    """
    Mengelola Enkripsi (AES-256-GCM) dan Key Derivation.
    """
    SALT_SIZE = 16
    NONCE_SIZE = 12
    ITERATIONS = 200000

    def __init__(self, password: str, salt: bytes = None):
        if salt is None:
            self.salt = os.urandom(self.SALT_SIZE)
        else:
            self.salt = salt
        
        self.key = self._derive_key(password, self.salt)
        self.aesgcm = AESGCM(self.key)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Menggunakan PBKDF2 untuk mengubah password menjadi key kriptografi."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.ITERATIONS,
        )
        return kdf.derive(password.encode())

    def encrypt(self, data: bytes) -> bytes:
        """Enkripsi data: nonce + ciphertext + tag (termasuk di AESGCM)."""
        nonce = os.urandom(self.NONCE_SIZE)
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        return nonce + ciphertext

    def decrypt(self, data: bytes) -> bytes:
        """Dekripsi data."""
        if len(data) < self.NONCE_SIZE:
            raise ValueError("Data terkorupsi atau terlalu pendek.")
        nonce = data[:self.NONCE_SIZE]
        ciphertext = data[self.NONCE_SIZE:]
        return self.aesgcm.decrypt(nonce, ciphertext, None)

    def get_salt(self) -> bytes:
        return self.salt
