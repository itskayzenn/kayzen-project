import os
import logging
from typing import Any, List, Dict
from .storage import StorageEngine
from .wal import WALManager
from .security import SecurityManager
from .cache import LRUCache

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KayzenDB:
    def __init__(self, db_path: str, password: str, cache_size: int = 1000):
        self.db_path = db_path
        self.wal_path = db_path + ".wal"
        
        self.storage = StorageEngine(db_path)
        self.wal = WALManager(self.wal_path)
        self.cache = LRUCache(cache_size)
        
        # Load Data & Security Context
        logging.info("Initializing KayzenDB...")
        self.data, self.security = self.storage.load(password)
        
        # Replay WAL if crash happened
        self._replay_wal()
        
        logging.info(f"DB Loaded. Records: {len(self.data)}")

    def _replay_wal(self):
        """Mengaplikasikan operasi yang belum tersimpan dari WAL."""
        entries = self.wal.replay()
        if not entries:
            return

        logging.info(f"Replaying {len(entries)} WAL entries...")
        for entry in entries:
            op, k, v = entry['op'], entry['k'], entry['v']
            if op == 'CREATE' or op == 'UPDATE':
                self.data[k] = v
            elif op == 'DELETE':
                if k in self.data:
                    del self.data[k]
        
        # Setelah replay sukses, lakukan checkpoint (simpan ke main DB) dan clear WAL
        self.checkpoint()

    def checkpoint(self):
        """Force save memory state to disk and clear WAL."""
        self.storage.save(self.data, self.security)
        self.wal.clear()

    def create(self, key: str, value: Dict[str, Any]):
        if key in self.data:
            raise ValueError(f"Key '{key}' already exists.")
        
        # 1. Write to WAL
        self.wal.log("CREATE", key, value)
        
        # 2. Update Memory & Cache
        self.data[key] = value
        self.cache.put(key, value)
        
        # 3. Checkpoint (Auto-commit strategy: bisa diubah jadi periodik untuk performa)
        self.checkpoint()

    def read(self, key: str) -> Dict[str, Any]:
        # 1. Check Cache
        cached = self.cache.get(key)
        if cached:
            return cached
        
        # 2. Check Memory
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found.")
        
        val = self.data[key]
        self.cache.put(key, val)
        return val

    def update(self, key: str, value: Dict[str, Any]):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found.")
        
        self.wal.log("UPDATE", key, value)
        self.data[key] = value
        self.cache.put(key, value)
        self.checkpoint()

    def delete(self, key: str):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found.")
        
        self.wal.log("DELETE", key)
        del self.data[key]
        self.cache.invalidate(key)
        self.checkpoint()

    def list_keys(self) -> List[str]:
        return list(self.data.keys())

    def find(self, field: str, operator: str, value: Any) -> List[Dict[str, Any]]:
        """
        Linear scan search.
        Operators: >, <, ==, !=
        """
        results = []
        for k, v in self.data.items():
            if not isinstance(v, dict) or field not in v:
                continue
            
            target = v[field]
            
            # Simple Type Coercion
            try:
                if isinstance(target, (int, float)) and isinstance(value, str):
                    check_val = float(value)
                else:
                    check_val = value
            except:
                check_val = value

            match = False
            if operator == "==": match = target == check_val
            elif operator == "!=": match = target != check_val
            elif operator == ">": match = target > check_val
            elif operator == "<": match = target < check_val
            
            if match:
                results.append({k: v})
                
        return results
