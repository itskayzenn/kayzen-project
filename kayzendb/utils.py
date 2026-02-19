import zlib
import json
from typing import Any

def calculate_checksum(data: bytes) -> int:
    """Menghitung CRC32 checksum dari data bytes."""
    return zlib.crc32(data)

def validate_checksum(data: bytes, expected_checksum: int) -> bool:
    """Memvalidasi integritas data."""
    return calculate_checksum(data) == expected_checksum

def serialize(data: Any) -> bytes:
    """Serialisasi data ke JSON bytes."""
    return json.dumps(data).encode('utf-8')

def deserialize(data: bytes) -> Any:
    """Deserialisasi JSON bytes ke objek Python."""
    return json.loads(data.decode('utf-8'))
