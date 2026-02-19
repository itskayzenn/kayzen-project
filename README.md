# kayzenDB

![banner](https://i.ibb.co.com/ZpmS4hQ7/kayzen-DB-20260219-122720-0000.png)

![kayzenDB](https://img.shields.io/badge/kayzenDB%20-%20black?logoSize=auto)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: AES-256-GCM](https://img.shields.io/badge/Security-AES--256--GCM-green.svg)](#-keamanan--acid)
[![Build: Docker](https://img.shields.io/badge/Build-Docker-blue.svg)](https://www.docker.com/)
[![Stability: ACID--Lite](https://img.shields.io/badge/Stability-ACID--Lite-orange.svg)](#-keamanan--acid)
[![Platform: Universal](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Cloud-lightgrey.svg)](#-instalasi-cepat-otomatis)

**kayzenDB** adalah database engine berbasis file yang dirancang untuk kecepatan, keamanan tingkat tinggi, dan portabilitas total. Menggabungkan kemudahan JSON dengan kekuatan enkripsi militer dan ketahanan data *Write-Ahead Logging* (WAL).

---

## Instalasi Cepat (Otomatis)

### A. Di Termux, Linux, atau MacOS
Gunakan skrip instalasi universal yang secara otomatis mendeteksi lingkungan Anda (termasuk penanganan otomatis Rust/Compiler di Termux):

```bash
chmod +x deploy_universal.sh
./deploy_universal.sh

B. Menggunakan Docker (Rekomendasi untuk Cloud/Railway)
Jalankan database tanpa perlu menginstal dependensi di host OS Anda:
# Build image
docker build -t kayzendb .

# Jalankan secara interaktif
docker run -it -v $(pwd)/data:/app/data kayzendb

## Penggunaan CLI (REPL)
Cukup jalankan perintah kayzen diikuti dengan nama file database Anda:
kayzen data/prod.kzn

Cheat Sheet Perintah:
| Perintah | Deskripsi | Contoh |
| :--- | :--- | :--- |
| CREATE | Menambah data baru | CREATE user1 {"name": "Zoro", "role": "Swordsman"} |
| READ | Mengambil data berdasarkan key | READ user1 |
| UPDATE | Memperbarui data yang ada | UPDATE user1 {"age": 21} |
| DELETE | Menghapus record | DELETE user1 |
| FIND | Pencarian dengan operator | FIND age > 20 |
| LIST | List semua key | LIST |

## Cloud Readiness & Backup
KayzenDB siap dideploy ke Railway.app menggunakan Dockerfile yang tersedia.

## Auto-Backup ke S3
Untuk mengaktifkan backup otomatis ke Cloud (AWS S3, Cloudflare R2, dll), atur Environment Variables berikut:
 * KAYZEN_S3_KEY: Access Key ID
 * KAYZEN_S3_SECRET: Secret Access Key
 * KAYZEN_S3_ENDPOINT: Endpoint URL
 * KAYZEN_BACKUP_BUCKET: Nama Bucket

## Keamanan & ACID
 * Atomicity: Menggunakan teknik rename-swap untuk memastikan file tidak pernah dalam kondisi setengah tertulis.
 * Consistency: Validasi CRC32 Checksums pada setiap sesi pembacaan data.
 * Isolation: Mekanisme single-writer lock untuk mencegah konflik data.
 * Durability: Implementasi WAL dan fsync menjamin data tetap selamat meski terjadi crash sistem.
 * Encryption: AES-256-GCM dengan derivasi kunci PBKDF2 (200,000 iterasi).

## Pengujian
Pastikan semua fungsi berjalan sempurna di lingkungan Anda:
pytest tests/

Author: Kayzen Izumi, itskayzenn, kayzenfry, sczkayzen
License: MIT

---
