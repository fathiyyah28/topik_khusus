"""
Comparison Service Module.

Module ini menangani perbandingan hasil pencarian
antara MongoDB dan Elasticsearch.
"""

import logging
from typing import List, Dict, Any, Tuple

from app import mongo_service as mongo
from app import elastic_service as es
from app.helper import hitung_waktu, cetak_hasil_pencarian

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def bandingkan_pencarian(keyword: str) -> None:
    """Membandingkan hasil pencarian MongoDB vs Elasticsearch.

    Fungsi ini akan:
    1. Mencari data di MongoDB menggunakan regex
    2. Mencari data di Elasticsearch menggunakan match query
    3. Menampilkan perbandingan hasil, jumlah, dan waktu

    Args:
        keyword: Kata kunci yang akan dicari.
    """
    print("\n" + "=" * 60)
    print(f"  PERBANDINGAN PENCARIAN: '{keyword}'")
    print("=" * 60)

    # --- Pencarian MongoDB ---
    print("\n[1] Mencari di MongoDB...")
    try:
        hasil_mongo, waktu_mongo = hitung_waktu(mongo.cari_regex, keyword)
        jumlah_mongo = len(hasil_mongo)
        cetak_hasil_pencarian(
            "MongoDB (Regex)", keyword,
            jumlah_mongo, hasil_mongo, waktu_mongo
        )
    except Exception as e:
        print(f"ERROR: {e}")
        hasil_mongo = []
        waktu_mongo = 0
        jumlah_mongo = 0

    # --- Pencarian Elasticsearch ---
    print("[2] Mencari di Elasticsearch...")
    try:
        hasil_es, waktu_es = hitung_waktu(es.cari_match, keyword)
        jumlah_es = len(hasil_es)
        cetak_hasil_pencarian(
            "Elasticsearch (Match Query)", keyword,
            jumlah_es, hasil_es, waktu_es
        )
    except Exception as e:
        print(f"ERROR: {e}")
        hasil_es = []
        waktu_es = 0
        jumlah_es = 0

    # --- Tabel Perbandingan ---
    tampilkan_tabel_perbandingan(
        keyword, jumlah_mongo, waktu_mongo, jumlah_es, waktu_es
    )

    # --- Kesimpulan ---
    tampilkan_kesimpulan(
        jumlah_mongo, waktu_mongo, jumlah_es, waktu_es
    )


def tampilkan_tabel_perbandingan(
    keyword: str,
    jumlah_mongo: int,
    waktu_mongo: float,
    jumlah_es: int,
    waktu_es: float
) -> None:
    """Menampilkan tabel perbandingan hasil pencarian.

    Args:
        keyword: Kata kunci yang dicari.
        jumlah_mongo: Jumlah hasil dari MongoDB.
        waktu_mongo: Waktu pencarian MongoDB (ms).
        jumlah_es: Jumlah hasil dari Elasticsearch.
        waktu_es: Waktu pencarian Elasticsearch (ms).
    """
    print("\n" + "=" * 60)
    print("  TABEL PERBANDINGAN")
    print("=" * 60)
    print(f"{'Aspek':<20} {'MongoDB':<20} {'Elasticsearch':<20}")
    print("-" * 60)
    print(f"{'Keyword':<20} {keyword:<20} {keyword:<20}")
    print(f"{'Jumlah Hasil':<20} {jumlah_mongo:<20} {jumlah_es:<20}")
    print(f"{'Waktu (ms)':<20} {waktu_mongo:<20} {waktu_es:<20}")
    print("=" * 60)


def tampilkan_kesimpulan(
    jumlah_mongo: int,
    waktu_mongo: float,
    jumlah_es: int,
    waktu_es: float
) -> None:
    """Menampilkan kesimpulan dari perbandingan.

    Args:
        jumlah_mongo: Jumlah hasil dari MongoDB.
        waktu_mongo: Waktu pencarian MongoDB (ms).
        jumlah_es: Jumlah hasil dari Elasticsearch.
        waktu_es: Waktu pencarian Elasticsearch (ms).
    """
    print("\n  KESIMPULAN")
    print("-" * 60)

    # Perbandingan jumlah hasil
    if jumlah_mongo > jumlah_es:
        print(f"  • MongoDB menemukan lebih banyak hasil "
              f"({jumlah_mongo} vs {jumlah_es}).")
    elif jumlah_es > jumlah_mongo:
        print(f"  • Elasticsearch menemukan lebih banyak hasil "
              f"({jumlah_es} vs {jumlah_mongo}).")
    else:
        print(f"  • Keduanya menemukan jumlah hasil yang sama "
              f"({jumlah_mongo}).")

    # Perbandingan waktu
    if waktu_mongo < waktu_es:
        print(f"  • MongoDB lebih cepat "
              f"({waktu_mongo} ms vs {waktu_es} ms).")
    elif waktu_es < waktu_mongo:
        print(f"  • Elasticsearch lebih cepat "
              f"({waktu_es} ms vs {waktu_mongo} ms).")
    else:
        print(f"  • Waktu pencarian sama "
              f"({waktu_mongo} ms).")

    # Analisis
    print("\n  ANALISIS:")
    print("  • MongoDB menggunakan regex untuk pattern matching")
    print("    pada field nama, kategori, dan spesifikasi.")
    print("  • Elasticsearch menggunakan full-text search")
    print("    dengan multi_match query dan analyzer standard.")
    print("  • Elasticsearch unggul untuk pencarian teks")
    print("    karena memiliki inverted index.")
    print("  • MongoDB unggul untuk pencarian exact match")
    print("    dan query terstruktur.")
    print("=" * 60)
    print()