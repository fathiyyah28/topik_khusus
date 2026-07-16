"""
Main Entry Point - Aplikasi MongoDB + Elasticsearch.

Aplikasi untuk membandingkan pencarian data antara MongoDB dan Elasticsearch
dengan studi kasus "Toko Peralatan Komputer".

Cara menjalankan:
    python app.py
"""

import json
import logging
import sys
import os
from typing import List, Dict, Any

from app import mongo_service as mongo
from app import elastic_service as es
from app import compare_service
from app.helper import (
    cetak_header,
    cetak_pemisah,
    input_pilihan,
    input_text,
    cetak_daftar_produk,
    format_harga
)

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- PATH DATASET ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "data", "products.json")


def muat_dataset() -> List[Dict[str, Any]]:
    """Memuat dataset dari file JSON.

    Returns:
        List dictionary data produk.
    """
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Dataset dimuat: {len(data)} produk.")
        return data
    except FileNotFoundError:
        print(f"ERROR: File dataset tidak ditemukan di {DATASET_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Format JSON tidak valid: {e}")
        return []


def menu_insert() -> None:
    """Insert dataset ke MongoDB dan index ke Elasticsearch."""
    cetak_header("INSERT DATASET")

    data = muat_dataset()
    if not data:
        print("Dataset kosong. Tidak ada data yang diinsert.")
        return

    print(f"Dataset berisi {len(data)} produk.")
    print()

    # Insert ke MongoDB
    try:
        jumlah_mongo = mongo.insert_banyak(data)
        print(f"✓ {jumlah_mongo} data berhasil diinsert ke MongoDB.")
    except Exception as e:
        print(f"✗ Gagal insert ke MongoDB: {e}")
        return

    # Index ke Elasticsearch
    try:
        jumlah_es = es.index_banyak(data)
        print(f"✓ {jumlah_es} data berhasil diindex ke Elasticsearch.")
    except Exception as e:
        print(f"✗ Gagal index ke Elasticsearch: {e}")

    print()
    print("Dataset berhasil diinsert dan diindex!")
    input("Tekan Enter untuk kembali ke menu...")


def menu_search_mongo() -> None:
    """Menu pencarian di MongoDB."""
    cetak_header("SEARCH MONGODB")

    # Cek koneksi
    if not mongo.cek_koneksi():
        print("✗ MongoDB belum berjalan.")
        print("  Pastikan MongoDB sudah dijalankan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    keyword = input_text("Masukkan kata kunci pencarian: ")

    from app.helper import hitung_waktu, cetak_hasil_pencarian

    try:
        hasil, waktu = hitung_waktu(mongo.cari_regex, keyword)
        jumlah = len(hasil)
        cetak_hasil_pencarian(
            "MongoDB (Regex)", keyword, jumlah, hasil, waktu
        )
    except Exception as e:
        print(f"ERROR: {e}")

    input("Tekan Enter untuk kembali ke menu...")


def menu_search_elastic() -> None:
    """Menu pencarian di Elasticsearch."""
    cetak_header("SEARCH ELASTICSEARCH")

    # Cek koneksi
    if not es.cek_koneksi():
        print("✗ Elasticsearch belum berjalan.")
        print("  Pastikan Elasticsearch sudah dijalankan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    keyword = input_text("Masukkan kata kunci pencarian: ")

    from app.helper import hitung_waktu, cetak_hasil_pencarian

    try:
        hasil, waktu = hitung_waktu(es.cari_match, keyword)
        jumlah = len(hasil)
        cetak_hasil_pencarian(
            "Elasticsearch (Match Query)", keyword, jumlah, hasil, waktu
        )
    except Exception as e:
        print(f"ERROR: {e}")

    input("Tekan Enter untuk kembali ke menu...")


def menu_bandingkan() -> None:
    """Menu perbandingan MongoDB vs Elasticsearch."""
    cetak_header("BANDINGKAN HASIL SEARCH")

    # Cek koneksi
    if not mongo.cek_koneksi():
        print("✗ MongoDB belum berjalan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if not es.cek_koneksi():
        print("✗ Elasticsearch belum berjalan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    keyword = input_text("Masukkan kata kunci pencarian: ")
    compare_service.bandingkan_pencarian(keyword)
    input("Tekan Enter untuk kembali ke menu...")


def menu_update() -> None:
    """Menu update data."""
    cetak_header("UPDATE DATA")

    # Cek koneksi
    if not mongo.cek_koneksi():
        print("✗ MongoDB belum berjalan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    try:
        # Tampilkan semua data
        data = mongo.cari_semua()
        if not data:
            print("Belum ada data. Silakan insert dataset terlebih dahulu.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        print("Data yang tersedia:")
        cetak_daftar_produk(data)
        print()

        produk_id = int(input("Masukkan ID produk yang akan diupdate: "))

        # Validasi ID
        produk_lama = None
        for p in data:
            if p["_id"] == produk_id:
                produk_lama = p
                break

        if produk_lama is None:
            print(f"Produk dengan ID {produk_id} tidak ditemukan.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        print(f"\nMengupdate: {produk_lama['nama']}")
        print("Kosongkan field jika tidak ingin mengubah.")
        print()

        nama_baru = input(f"Nama [{produk_lama['nama']}]: ").strip()
        kategori_baru = input(
            f"Kategori [{produk_lama['kategori']}]: "
        ).strip()
        harga_input = input(
            f"Harga [{produk_lama['harga']}]: "
        ).strip()
        stok_input = input(
            f"Stok [{produk_lama['stok']}]: "
        ).strip()
        spesifikasi_baru = input(
            f"Spesifikasi [{produk_lama['spesifikasi']}]: "
        ).strip()

        # Siapkan data update (hanya field yang diisi)
        data_baru = {}
        if nama_baru:
            data_baru["nama"] = nama_baru
        if kategori_baru:
            data_baru["kategori"] = kategori_baru
        if harga_input:
            data_baru["harga"] = int(harga_input)
        if stok_input:
            data_baru["stok"] = int(stok_input)
        if spesifikasi_baru:
            data_baru["spesifikasi"] = spesifikasi_baru

        if not data_baru:
            print("Tidak ada perubahan.")
        else:
            # Update MongoDB
            berhasil_mongo = mongo.update_data(produk_id, data_baru)
            if berhasil_mongo:
                print("✓ Berhasil update di MongoDB.")
            else:
                print("✗ Gagal update di MongoDB.")

            # Update Elasticsearch
            berhasil_es = es.update_data(produk_id, data_baru)
            if berhasil_es:
                print("✓ Berhasil update di Elasticsearch.")
            else:
                print("✗ Gagal update di Elasticsearch.")

    except ValueError:
        print("ERROR: ID harus berupa angka.")
    except Exception as e:
        print(f"ERROR: {e}")

    input("Tekan Enter untuk kembali ke menu...")


def menu_delete() -> None:
    """Menu delete data."""
    cetak_header("DELETE DATA")

    # Cek koneksi
    if not mongo.cek_koneksi():
        print("✗ MongoDB belum berjalan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    try:
        # Tampilkan semua data
        data = mongo.cari_semua()
        if not data:
            print("Belum ada data. Silakan insert dataset terlebih dahulu.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        print("Data yang tersedia:")
        for p in data:
            print(f"  ID {p['_id']}: {p['nama']}")
        print()

        produk_id = int(input("Masukkan ID produk yang akan dihapus: "))

        # Konfirmasi
        konfirmasi = input(
            f"Yakin ingin menghapus ID {produk_id}? (y/n): "
        ).strip().lower()
        if konfirmasi != "y":
            print("Penghapusan dibatalkan.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        # Delete dari MongoDB
        berhasil_mongo = mongo.delete_data(produk_id)
        if berhasil_mongo:
            print("✓ Berhasil hapus dari MongoDB.")
        else:
            print("✗ Gagal hapus dari MongoDB (ID tidak ditemukan).")

        # Delete dari Elasticsearch
        try:
            berhasil_es = es.delete_data(produk_id)
            if berhasil_es:
                print("✓ Berhasil hapus dari Elasticsearch.")
            else:
                print("✗ Gagal hapus dari Elasticsearch.")
        except Exception as e:
            print(f"✗ Gagal hapus dari Elasticsearch: {e}")

    except ValueError:
        print("ERROR: ID harus berupa angka.")
    except Exception as e:
        print(f"ERROR: {e}")

    input("Tekan Enter untuk kembali ke menu...")


def menu_utama() -> None:
    """Menampilkan menu utama aplikasi."""
    while True:
        cetak_header("MongoDB + Elasticsearch Demo")
        print("  Aplikasi Perbandingan Pencarian Data")
        print("  Topik: Toko Peralatan Komputer")
        print()
        print("  1. Insert Dataset")
        print("  2. Search MongoDB")
        print("  3. Search Elasticsearch")
        print("  4. Bandingkan Hasil Search")
        print("  5. Update Data")
        print("  6. Delete Data")
        print("  7. Keluar")
        print()

        pilihan = input_pilihan("Pilih menu [1-7]: ", 1, 7)
        print()

        if pilihan == 1:
            menu_insert()
        elif pilihan == 2:
            menu_search_mongo()
        elif pilihan == 3:
            menu_search_elastic()
        elif pilihan == 4:
            menu_bandingkan()
        elif pilihan == 5:
            menu_update()
        elif pilihan == 6:
            menu_delete()
        elif pilihan == 7:
            print("Terima kasih telah menggunakan aplikasi ini!")
            print("MongoDB + Elasticsearch Demo - Topik Khusus")
            break


def main() -> None:
    """Main function untuk menjalankan aplikasi."""
    try:
        menu_utama()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Terjadi error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()