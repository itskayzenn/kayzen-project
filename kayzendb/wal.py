import os
import time
import json
from typing import List, Dict, Any

class WALManager:
    """
    Menangani Write-Ahead Logging.
    Format Log: Timestamp|Op|Key|ValueJSON\n
    """
    def __init__(self, wal_path: str):
        self.wal_path = wal_path

    def log(self, operation: str, key: str, value: Any = None):
        """Mencatat operasi ke WAL dan melakukan fsync."""
        entry = {
            "ts": time.time(),
            "op": operation,
            "k": key,
            "v": value
        }
        line = json.dumps(entry) + "\n"
        
        with open(self.wal_path, "a") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno()) # Durability: Force write to disk

    def replay(self) -> List[Dict[str, Any]]:
        """Membaca log untuk recovery saat startup."""
        if not os.path.exists(self.wal_path):
            return []
        
        entries = []
        try:
            with open(self.wal_path, "r") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
        except json.JSONDecodeError:
            print("Warning: WAL corrupted specific entry ignored.")
        return entries

    def clear(self):
        """Membersihkan WAL setelah checkpoint berhasil."""
        open(self.wal_path, 'w').close()
