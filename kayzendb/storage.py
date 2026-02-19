import os
import zlib
import struct
from .security import SecurityManager
from .utils import calculate_checksum, validate_checksum, serialize, deserialize

class StorageEngine:
    """
    Mengelola persistensi data ke disk dengan:
    - Kompresi (zlib)
    - Enkripsi (AES-GCM)
    - Checksum (CRC32)
    - Atomic Write (Rename-Swap)
    """
    HEADER_FORMAT = "!16sI" # 16 bytes Salt + 4 bytes CRC32
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, db_path: str):
        self.db_path = db_path

    def save(self, data: dict, security: SecurityManager):
        """Atomic Save: Serialize -> Compress -> Encrypt -> Write Temp -> Rename."""
        # 1. Serialize
        raw_bytes = serialize(data)
        
        # 2. Compress
        compressed_data = zlib.compress(raw_bytes)
        
        # 3. Encrypt
        encrypted_data = security.encrypt(compressed_data)
        
        # 4. Calculate Checksum (on encrypted data)
        checksum = calculate_checksum(encrypted_data)
        
        # 5. Prepare Header (Salt + Checksum)
        salt = security.get_salt()
        header = struct.pack(self.HEADER_FORMAT, salt, checksum)
        
        # 6. Write to Temp File
        temp_path = self.db_path + ".tmp"
        with open(temp_path, "wb") as f:
            f.write(header)
            f.write(encrypted_data)
            f.flush()
            os.fsync(f.fileno())
            
        # 7. Atomic Rename (Windows: replace, Unix: rename)
        os.replace(temp_path, self.db_path)

    def load(self, password: str) -> tuple[dict, SecurityManager]:
        """Load: Read -> Validate Checksum -> Decrypt -> Decompress -> Deserialize."""
        if not os.path.exists(self.db_path):
            # Init new DB
            sec = SecurityManager(password)
            return {}, sec

        with open(self.db_path, "rb") as f:
            # Read Header
            header_bytes = f.read(self.HEADER_SIZE)
            salt, stored_checksum = struct.unpack(self.HEADER_FORMAT, header_bytes)
            
            # Read Body
            encrypted_data = f.read()

        # Validate Integrity
        if not validate_checksum(encrypted_data, stored_checksum):
            raise ValueError("CRITICAL: Data corruption detected! Checksum mismatch.")

        # Init Security with stored salt
        security = SecurityManager(password, salt)

        try:
            # Decrypt
            compressed_data = security.decrypt(encrypted_data)
            # Decompress
            raw_bytes = zlib.decompress(compressed_data)
            # Deserialize
            data = deserialize(raw_bytes)
            return data, security
        except Exception as e:
            raise ValueError(f"Failed to load database. Wrong password or corruption. Error: {e}")
