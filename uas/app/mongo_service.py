"""
MongoDB Service Module.

Module ini menangani seluruh operasi CRUD dan pencarian
pada MongoDB menggunakan library pymongo.
"""

import logging
from typing import List, Dict, Any, Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from pymongo.collection import Collection

from app.config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def dapatkan_koneksi() -> Optional[MongoClient]:
    """Mendapatkan koneksi ke MongoDB.

    Returns:
        MongoClient jika berhasil, None jika gagal.

    Raises:
        ConnectionFailure: Jika MongoDB tidak dapat dihubungi.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Tes koneksi
        client.admin.command("ping")
        logger.info("Berhasil terhubung ke MongoDB.")
        return client
    except ConnectionFailure:
        logger.error("Gagal terhubung ke MongoDB.")
        return None


def dapatkan_koleksi() -> Optional[Collection]:
    """Mendapatkan collection MongoDB.

    Returns:
        Collection object jika berhasil, None jika gagal.
    """
    client = dapatkan_koneksi()
    if client is None:
        return None
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION_NAME]


def insert_banyak(data_list: List[Dict[str, Any]]) -> int:
    """Insert banyak data ke MongoDB.

    Args:
        data_list: List dictionary data yang akan diinsert.

    Returns:
        Jumlah data yang berhasil diinsert.

    Raises:
        ConnectionFailure: Jika MongoDB belum berjalan.
    """
    collection = dapatkan_koleksi()
    if collection is None:
        raise ConnectionFailure("MongoDB belum berjalan.")

    try:
        # Hapus data lama agar tidak duplikat
        collection.delete_many({})
        logger.info("Data lama dihapus.")

        result = collection.insert_many(data_list)
        jumlah = len(result.inserted_ids)
        logger.info(f"Berhasil insert {jumlah} data ke MongoDB.")
        return jumlah
    except PyMongoError as e:
        logger.error(f"Gagal insert data: {e}")
        raise


def cari_semua() -> List[Dict[str, Any]]:
    """Mengambil semua data dari MongoDB.

    Returns:
        List semua produk.

    Raises:
        ConnectionFailure: Jika MongoDB belum berjalan.
    """
    collection = dapatkan_koleksi()
    if collection is None:
        raise ConnectionFailure("MongoDB belum berjalan.")

    try:
        data = list(collection.find({}))
        logger.info(f"Data ditemukan: {len(data)} produk.")
        return data
    except PyMongoError as e:
        logger.error(f"Gagal mengambil data: {e}")
        return []


def cari_regex(keyword: str) -> List[Dict[str, Any]]:
    """Mencari data menggunakan regex di MongoDB.

    Melakukan pencarian pada field 'nama', 'kategori',
    dan 'spesifikasi' menggunakan regex case-insensitive.

    Args:
        keyword: Kata kunci pencarian.

    Returns:
        List produk yang cocok dengan keyword.

    Raises:
        ConnectionFailure: Jika MongoDB belum berjalan.
    """
    collection = dapatkan_koleksi()
    if collection is None:
        raise ConnectionFailure("MongoDB belum berjalan.")

    try:
        import re
        pattern = re.compile(keyword, re.IGNORECASE)
        query = {
            "$or": [
                {"nama": {"$regex": pattern}},
                {"kategori": {"$regex": pattern}},
                {"spesifikasi": {"$regex": pattern}}
            ]
        }
        data = list(collection.find(query))
        logger.info(f"Pencarian MongoDB '{keyword}': {len(data)} hasil.")
        return data
    except PyMongoError as e:
        logger.error(f"Gagal mencari data: {e}")
        return []


def update_data(produk_id: int, data_baru: Dict[str, Any]) -> bool:
    """Update data produk berdasarkan ID.

    Args:
        produk_id: ID produk yang akan diupdate.
        data_baru: Dictionary berisi field yang akan diupdate.

    Returns:
        True jika berhasil, False jika gagal.

    Raises:
        ConnectionFailure: Jika MongoDB belum berjalan.
    """
    collection = dapatkan_koleksi()
    if collection is None:
        raise ConnectionFailure("MongoDB belum berjalan.")

    try:
        result = collection.update_one(
            {"_id": produk_id},
            {"$set": data_baru}
        )
        if result.modified_count > 0:
            logger.info(f"Data ID {produk_id} berhasil diupdate.")
            return True
        else:
            logger.warning(f"Data ID {produk_id} tidak ditemukan.")
            return False
    except PyMongoError as e:
        logger.error(f"Gagal update data: {e}")
        return False


def delete_data(produk_id: int) -> bool:
    """Hapus data produk berdasarkan ID.

    Args:
        produk_id: ID produk yang akan dihapus.

    Returns:
        True jika berhasil, False jika gagal.

    Raises:
        ConnectionFailure: Jika MongoDB belum berjalan.
    """
    collection = dapatkan_koleksi()
    if collection is None:
        raise ConnectionFailure("MongoDB belum berjalan.")

    try:
        result = collection.delete_one({"_id": produk_id})
        if result.deleted_count > 0:
            logger.info(f"Data ID {produk_id} berhasil dihapus.")
            return True
        else:
            logger.warning(f"Data ID {produk_id} tidak ditemukan.")
            return False
    except PyMongoError as e:
        logger.error(f"Gagal hapus data: {e}")
        return False


def cek_koneksi() -> bool:
    """Cek apakah MongoDB dapat diakses.

    Returns:
        True jika terkoneksi, False jika tidak.
    """
    client = dapatkan_koneksi()
    if client:
        client.close()
        return True
    return False