#!/bin/bash

echo "🌌 KayzenDB Universal Deployer"
echo "------------------------------"

# Cek apakah Docker terinstall
if command -v docker &> /dev/null
then
    echo "🐳 Docker terdeteksi. Membangun container..."
    docker build -t kayzendb-app .
    echo "✅ Build selesai."
    echo "🚀 Jalankan dengan: docker run -it -v $(pwd)/data:/app/data kayzendb-app"
else
    echo "⚠️ Docker tidak ditemukan. Mencoba instalasi Python lokal..."
    
    # Deteksi OS
    OS="$(uname)"
    if [ "$OS" == "Linux" ]; then
        sudo apt-get update && sudo apt-get install -y python3-pip build-essential libssl-dev libffi-dev
    elif [ "$OS" == "Darwin" ]; then
        brew install python
    fi

    pip install cryptography pytest
    pip install -e .
    echo "✅ Instalasi lokal selesai."
    echo "🚀 Jalankan dengan: kayzen my_database.kzn"
fi
