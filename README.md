# KayzenDB

Lightweight, Secure, ACID-lite File-Based Database Engine.

## Fitur
* **Keamanan**: AES-256-GCM encryption + PBKDF2 Key Derivation.
* **Integritas**: CRC32 Checksums untuk setiap block data.
* **Durabilitas**: Write-Ahead Logging (WAL) + Atomic Commit.
* **Performa**: In-memory Indexing + LRU Caching + Compression.

## Instalasi

```bash
pip install .

Penggunaan CLI
# Jalankan database
kayzen mydatabase.kzn

# Masukkan password saat diminta (password baru untuk DB baru)

Perintah dalam REPL:
kayzen> CREATE u1 {"name": "Budi", "age": 25, "city": "Jakarta"}
kayzen> READ u1
kayzen> UPDATE u1 {"name": "Budi Hartono", "age": 26, "city": "Jakarta"}
kayzen> FIND age > 20
kayzen> DELETE u1

Testing
pytest tests/


### Analisis Kualitas & Arsitektur

1.  **Separation of Concerns**:
    * `StorageEngine` hanya peduli byte fisik (encrypt/compress/write).
    * `WALManager` hanya peduli logging append-only.
    * `SecurityManager` hanya peduli kriptografi.
    * `KayzenDB` (Core) bertindak sebagai orkestrator.
2.  **ACID-Lite**:
    * *Atomicity*: Dicapai lewat `os.replace` (atomic rename) di `StorageEngine`.
    * *Consistency*: Checksum validation saat load.
    * *Isolation*: Single-process lock (implisit via penggunaan file lock jika diperluas, saat ini basic single-instance).
    * *Durability*: `os.fsync` di WAL.
3.  **Security**: Menggunakan standar industri (AES-GCM) dan salt yang unik per file database.

Solusi ini siap digunakan sebagai fondasi database engine lokal yang serius.

# kayzen-project
