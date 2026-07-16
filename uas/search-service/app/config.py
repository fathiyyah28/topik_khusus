"""
Configuration for Search Service.

Membaca konfigurasi dari environment variable.
"""

import os


# --- Elasticsearch Configuration ---
ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "localhost")
ELASTIC_PORT: int = int(os.getenv("ELASTIC_PORT", "9200"))
ELASTIC_INDEX_NAME: str = os.getenv("ELASTIC_INDEX_NAME", "produk")

ELASTIC_URI: str = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}/"

# --- Server Configuration ---
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8002"))