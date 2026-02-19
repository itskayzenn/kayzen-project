import os
import boto3
import tarfile
from datetime import datetime

# Konfigurasi - Sebaiknya gunakan Environment Variables di Railway/Docker
S3_BUCKET = os.getenv("KAYZEN_BACKUP_BUCKET", "my-kayzen-backups")
S3_ACCESS_KEY = os.getenv("KAYZEN_S3_KEY")
S3_SECRET_KEY = os.getenv("KAYZEN_S3_SECRET")
S3_ENDPOINT = os.getenv("KAYZEN_S3_ENDPOINT") # Contoh: https://r2.cloudflarestorage.com

def create_backup(db_file: str):
    """Membuat tarball dari DB dan WAL file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_kayzen_{timestamp}.tar.gz"
    
    with tarfile.open(backup_filename, "w:gz") as tar:
        tar.add(db_file)
        if os.path.exists(db_file + ".wal"):
            tar.add(db_file + ".wal")
            
    return backup_filename

def upload_to_s3(file_name: str):
    """Upload file ke S3 storage."""
    if not all([S3_ACCESS_KEY, S3_SECRET_KEY]):
        print("⚠️ S3 Credentials tidak ditemukan. Backup lokal saja.")
        return

    s3 = boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )
    
    try:
        s3.upload_file(file_name, S3_BUCKET, file_name)
        print(f"✅ Backup berhasil diupload: {file_name}")
        os.remove(file_name) # Hapus file lokal setelah upload
    except Exception as e:
        print(f"❌ Gagal upload backup: {e}")

if __name__ == "__main__":
    # Ganti dengan path database Anda
    db_path = "data/prod.kzn"
    if os.path.exists(db_path):
        fname = create_backup(db_path)
        upload_to_s3(fname)
