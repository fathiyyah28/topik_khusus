"""
Elasticsearch Service Module.

Module ini menangani seluruh operasi indexing, pencarian,
update, dan delete pada Elasticsearch menggunakan library elasticsearch.
"""

import logging
from typing import List, Dict, Any, Optional

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

from app.config import ELASTIC_URI, ELASTIC_INDEX_NAME

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def dapatkan_koneksi() -> Optional[Elasticsearch]:
    """Mendapatkan koneksi ke Elasticsearch.

    Returns:
        Elasticsearch client jika berhasil, None jika gagal.
    """
    try:
        client = Elasticsearch(ELASTIC_URI)
        # Tes koneksi
        if client.ping():
            logger.info("Berhasil terhubung ke Elasticsearch.")
            return client
        else:
            logger.error("Gagal terhubung ke Elasticsearch.")
            return None
    except ConnectionError:
        logger.error("Gagal terhubung ke Elasticsearch.")
        return None


def buat_index() -> bool:
    """Membuat index Elasticsearch jika belum ada.

    Mendefinisikan mapping untuk field-field produk
    agar pencarian lebih optimal.

    Returns:
        True jika berhasil, False jika gagal.
    """
    client = dapatkan_koneksi()
    if client is None:
        return False

    try:
        if not client.indices.exists(index=ELASTIC_INDEX_NAME):
            mapping = {
                "mappings": {
                    "properties": {
                        "_id": {"type": "integer"},
                        "nama": {"type": "text", "analyzer": "standard"},
                        "kategori": {"type": "text", "analyzer": "standard"},
                        "harga": {"type": "integer"},
                        "stok": {"type": "integer"},
                        "spesifikasi": {
                            "type": "text",
                            "analyzer": "standard"
                        }
                    }
                }
            }
            client.indices.create(index=ELASTIC_INDEX_NAME, body=mapping)
            logger.info(f"Index '{ELASTIC_INDEX_NAME}' berhasil dibuat.")
        else:
            logger.info(f"Index '{ELASTIC_INDEX_NAME}' sudah ada.")
        return True
    except Exception as e:
        logger.error(f"Gagal membuat index: {e}")
        return False


def index_banyak(data_list: List[Dict[str, Any]]) -> int:
    """Index banyak data ke Elasticsearch.

    Args:
        data_list: List dictionary data yang akan diindex.

    Returns:
        Jumlah data yang berhasil diindex.

    Raises:
        ConnectionError: Jika Elasticsearch belum berjalan.
    """
    client = dapatkan_koneksi()
    if client is None:
        raise ConnectionError("Elasticsearch belum berjalan.")

    # Buat index jika belum ada
    buat_index()

    try:
        # Hapus index lama agar tidak duplikat
        if client.indices.exists(index=ELASTIC_INDEX_NAME):
            client.indices.delete(index=ELASTIC_INDEX_NAME)
            logger.info("Index lama dihapus.")
        buat_index()

        jumlah = 0
        for data in data_list:
            doc_id = data["_id"]
            client.index(
                index=ELASTIC_INDEX_NAME,
                id=doc_id,
                body=data
            )
            jumlah += 1

        # Refresh agar data langsung bisa dicari
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        logger.info(f"Berhasil index {jumlah} data ke Elasticsearch.")
        return jumlah
    except Exception as e:
        logger.error(f"Gagal index data: {e}")
        raise


def cari_match(keyword: str) -> List[Dict[str, Any]]:
    """Mencari data menggunakan match query di Elasticsearch.

    Melakukan pencarian full-text pada field 'nama', 'kategori',
    dan 'spesifikasi'.

    Args:
        keyword: Kata kunci pencarian.

    Returns:
        List produk yang cocok dengan keyword.

    Raises:
        ConnectionError: Jika Elasticsearch belum berjalan.
    """
    client = dapatkan_koneksi()
    if client is None:
        raise ConnectionError("Elasticsearch belum berjalan.")

    try:
        query = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["nama", "kategori", "spesifikasi"],
                    "type": "best_fields"
                }
            }
        }
        response = client.search(
            index=ELASTIC_INDEX_NAME,
            body=query
        )

        hits = response["hits"]["hits"]
        data = [hit["_source"] for hit in hits]
        logger.info(f"Pencarian ES '{keyword}': {len(data)} hasil.")
        return data
    except NotFoundError:
        logger.warning(f"Index '{ELASTIC_INDEX_NAME}' tidak ditemukan.")
        return []
    except Exception as e:
        logger.error(f"Gagal mencari data: {e}")
        return []


def update_data(produk_id: int, data_baru: Dict[str, Any]) -> bool:
    """Update data di Elasticsearch berdasarkan ID.

    Args:
        produk_id: ID produk yang akan diupdate.
        data_baru: Dictionary berisi field yang akan diupdate.

    Returns:
        True jika berhasil, False jika gagal.

    Raises:
        ConnectionError: Jika Elasticsearch belum berjalan.
    """
    client = dapatkan_koneksi()
    if client is None:
        raise ConnectionError("Elasticsearch belum berjalan.")

    try:
        client.update(
            index=ELASTIC_INDEX_NAME,
            id=produk_id,
            body={"doc": data_baru}
        )
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        logger.info(f"Data ID {produk_id} berhasil diupdate di ES.")
        return True
    except NotFoundError:
        logger.warning(f"Data ID {produk_id} tidak ditemukan di ES.")
        return False
    except Exception as e:
        logger.error(f"Gagal update data di ES: {e}")
        return False


def delete_data(produk_id: int) -> bool:
    """Hapus data di Elasticsearch berdasarkan ID.

    Args:
        produk_id: ID produk yang akan dihapus.

    Returns:
        True jika berhasil, False jika gagal.

    Raises:
        ConnectionError: Jika Elasticsearch belum berjalan.
    """
    client = dapatkan_koneksi()
    if client is None:
        raise ConnectionError("Elasticsearch belum berjalan.")

    try:
        client.delete(
            index=ELASTIC_INDEX_NAME,
            id=produk_id
        )
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        logger.info(f"Data ID {produk_id} berhasil dihapus dari ES.")
        return True
    except NotFoundError:
        logger.warning(f"Data ID {produk_id} tidak ditemukan di ES.")
        return False
    except Exception as e:
        logger.error(f"Gagal hapus data di ES: {e}")
        return False


def cek_koneksi() -> bool:
    """Cek apakah Elasticsearch dapat diakses.

    Returns:
        True jika terkoneksi, False jika tidak.
    """
    client = dapatkan_koneksi()
    if client:
        client.close()
        return True
    return False