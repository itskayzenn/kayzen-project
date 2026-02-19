# Gunakan base image Python yang ringan
FROM python:3.12-slim-bookworm

# Install build dependencies (Rust & OpenSSL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tambahkan Rust ke PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Tentukan direktori kerja
WORKDIR /app

# Salin file proyek
COPY . .

# Install dependensi & KayzenDB
RUN pip install --no-cache-dir cryptography pytest
RUN pip install -e .

# Volume untuk persistensi data database
VOLUME ["/app/data"]

# Default command: Menjalankan REPL (Opsional)
# Untuk Railway/Cloud, kita biasanya menggunakan script start
CMD ["kayzen", "/app/data/prod.kzn"]
