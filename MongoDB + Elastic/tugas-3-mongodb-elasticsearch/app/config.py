"""
Konfigurasi koneksi untuk MongoDB dan Elasticsearch.

Module ini menyimpan semua konfigurasi yang diperlukan
untuk terhubung ke MongoDB dan Elasticsearch.
"""

# Konfigurasi MongoDB
MONGO_HOST: str = "localhost"
MONGO_PORT: int = 27017
MONGO_DB_NAME: str = "toko_komputer"
MONGO_COLLECTION_NAME: str = "produk"

# Konfigurasi Elasticsearch
ELASTIC_HOST: str = "localhost"
ELASTIC_PORT: int = 9200
ELASTIC_INDEX_NAME: str = "produk"

# URL koneksi
MONGO_URI: str = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
ELASTIC_URI: str = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"