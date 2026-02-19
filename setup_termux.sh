#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Memperbaiki setup KayzenDB untuk Termux..."

# 1. Update Repo
pkg update -y

# 2. Install Python, Rust, dan Compiler penting
echo "🛠️ Menginstall Python, Rust, dan Build Tools..."
pkg install -y python clang rust make libffi openssl binutils-is-llvm

# 3. Install Cryptography via PKG (PENTING: Menghindari error build Rust)
echo "📦 Menginstall python-cryptography via pkg..."
pkg install -y python-cryptography

# 4. Install sisa dependensi via Pip
echo "📚 Menginstall pytest..."
pip install pytest

# 5. Install KayzenDB
if [ -f "setup.py" ]; then
    echo "🏗️ Menginstall KayzenDB package..."
    pip install -e .
fi

echo "🧪 Menjalankan verifikasi..."
pytest tests/

echo "======================================================"
echo "🎉 Setup Selesai!"
echo "Gunakan perintah: kayzen mydb.kzn"
echo "======================================================"
