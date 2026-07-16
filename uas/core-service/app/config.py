"""
Configuration for Core Service.

Membaca konfigurasi dari environment variable.
Menggunakan fallback ke default value untuk development.
"""

import os


# --- MongoDB Configuration ---
MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT: int = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "toko_komputer")
MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "produk")

MONGO_URI: str = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

# --- Search Service URL ---
SEARCH_SERVICE_URL: str = os.getenv("SEARCH_SERVICE_URL", "http://localhost:8002")

# --- Server Configuration ---
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8001"))

# --- Dataset Path ---
# Default: relative to project root, override with DATASET_PATH env var
DATASET_PATH: str = os.getenv(
    "DATASET_PATH",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                 "data", "products.json")
)
