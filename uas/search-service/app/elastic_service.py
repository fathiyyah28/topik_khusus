"""
Elasticsearch Service Module.

Menangani seluruh operasi indexing, pencarian, update, dan delete
pada Elasticsearch. Di-refactor dari app/elastic_service.py project lama.
"""

import logging
from typing import List, Dict, Any, Optional

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

from app.config import ELASTIC_URI, ELASTIC_INDEX_NAME

logger = logging.getLogger(__name__)


def dapatkan_koneksi() -> Optional[Elasticsearch]:
    """Mendapatkan koneksi ke Elasticsearch.

    Returns:
        Elasticsearch client jika berhasil, None jika gagal.
    """
    try:
        client = Elasticsearch(ELASTIC_URI)
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

    buat_index()

    try:
        # Hapus index lama
        if client.indices.exists(index=ELASTIC_INDEX_NAME):
            client.indices.delete(index=ELASTIC_INDEX_NAME)
            logger.info("Index lama dihapus.")
        buat_index()

        jumlah = 0
        for data in data_list:
            doc_id = data["_id"]
            # Buat copy data tanpa _id untuk body (Elasticsearch menganggap _id sebagai metadata)
            doc_body = {k: v for k, v in data.items() if k != "_id"}
            client.index(
                index=ELASTIC_INDEX_NAME,
                id=doc_id,
                body=doc_body
            )
            jumlah += 1

        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        logger.info(f"Berhasil index {jumlah} data ke Elasticsearch.")
        return jumlah
    except Exception as e:
        logger.error(f"Gagal index data: {e}")
        raise


def index_satu(produk: Dict[str, Any]) -> bool:
    """Index satu produk ke Elasticsearch.

    Args:
        produk: Dictionary data produk.

    Returns:
        True jika berhasil, False jika gagal.

    Raises:
        ConnectionError: Jika Elasticsearch belum berjalan.
    """
    client = dapatkan_koneksi()
    if client is None:
        raise ConnectionError("Elasticsearch belum berjalan.")

    buat_index()

    try:
        doc_id = produk["_id"]
        # Buat copy data tanpa _id untuk body (Elasticsearch menganggap _id sebagai metadata)
        doc_body = {k: v for k, v in produk.items() if k != "_id"}
        client.index(
            index=ELASTIC_INDEX_NAME,
            id=doc_id,
            body=doc_body
        )
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        logger.info(f"Berhasil index produk ID {doc_id} ke ES.")
        return True
    except Exception as e:
        logger.error(f"Gagal index produk: {e}")
        return False


def cari_match(keyword: str) -> List[Dict[str, Any]]:
    """Mencari data menggunakan multi_match query di Elasticsearch.

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
        return True
    return False


def dapatkan_stats() -> Dict[str, Any]:
    """Mendapatkan statistik index Elasticsearch.

    Returns:
        Dictionary berisi statistik index.
    """
    client = dapatkan_koneksi()
    if client is None:
        return {"status": "disconnected"}

    try:
        if not client.indices.exists(index=ELASTIC_INDEX_NAME):
            return {"status": "no_index", "index": ELASTIC_INDEX_NAME}

        stats = client.indices.stats(index=ELASTIC_INDEX_NAME)
        index_stats = stats["indices"][ELASTIC_INDEX_NAME]["total"]

        return {
            "status": "connected",
            "index": ELASTIC_INDEX_NAME,
            "document_count": index_stats["docs"]["count"],
            "size_in_bytes": index_stats["store"]["size_in_bytes"]
        }
    except Exception as e:
        logger.error(f"Gagal mendapatkan stats: {e}")
        return {"status": "error", "message": str(e)}