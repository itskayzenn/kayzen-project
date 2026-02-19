# kayzenDB

<p align="center">
  <img src="https://i.ibb.co.com/ZpmS4hQ7/kayzen-DB-20260219-122720-0000.png" width="600"/>
</p>

<p align="center">

  ![Engine](https://img.shields.io/badge/Engine-kayzenDB-black?style=for-the-badge)
  ![Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
  ![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
  ![Security](https://img.shields.io/badge/Encryption-AES--256--GCM-green?style=for-the-badge)
  ![ACID](https://img.shields.io/badge/Stability-ACID--Lite-orange?style=for-the-badge)
  ![WAL](https://img.shields.io/badge/Storage-WAL-red?style=for-the-badge)
  ![Docker](https://img.shields.io/badge/Build-Docker-blue?style=for-the-badge&logo=docker)
  ![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Cloud-lightgrey?style=for-the-badge)
  ![CLI](https://img.shields.io/badge/Interface-CLI-purple?style=for-the-badge)
  ![Backup](https://img.shields.io/badge/Backup-S3%20Compatible-blue?style=for-the-badge&logo=amazonaws)

</p>

---

<p align="center">
  ⚡ File-Based Database Engine • 🔐 Military-Grade Encryption • 💾 WAL Durability • ☁ Cloud Ready
</p>

---

## 🚀 Instalasi Cepat

### 🖥 Termux / Linux / MacOS
```bash
chmod +x deploy_universal.sh
./deploy_universal.sh
```

🐳 Docker (Cloud / Railway)

docker build -t kayzendb .
docker run -it -v $(pwd)/data:/app/data kayzendb

💻 Penggunaan CLI

kayzen data/prod.kzn

📌 Command Cheat Sheet

Command	Fungsi
```
CREATE	Tambah data
READ	Ambil data
UPDATE	Update data
DELETE	Hapus data
FIND	Query dengan operator
LIST	Tampilkan semua key
```

☁ Cloud Ready

Dockerfile Included
Railway Compatible
S3 / Cloudflare R2 Backup


🔑 Environment Variables
```
KAYZEN_S3_KEY
KAYZEN_S3_SECRET
KAYZEN_S3_ENDPOINT
KAYZEN_BACKUP_BUCKET
```

🔐 Security & ACID-lite

Feature	Implementasi

Atomicity	Rename-Swap
Consistency	CRC32 Validation
Isolation	Single Writer Lock
Durability	WAL + fsync
Encryption	AES-256-GCM + PBKDF2 (200k iterasi)

🧪 Testing
```
pytest tests/
```

<p align="center">
  Made with ⚙ by Kayzen Izumi  
  MIT License
</p>
