"""
Helper functions untuk aplikasi MongoDB + Elasticsearch.

Berisi fungsi-fungsi bantu seperti:
- Pengecekan koneksi database
- Formatting output
- Cetak tabel hasil pencarian
"""

import time
from typing import List, Dict, Any


def format_harga(harga: int) -> str:
    """Format angka harga ke format Rupiah.

    Args:
        harga: Harga dalam integer.

    Returns:
        String harga dengan format Rp x.xxx.xxx
    """
    return f"Rp {harga:,.0f}".replace(",", ".")


def hitung_waktu(func: callable, *args, **kwargs) -> tuple:
    """Hitung waktu eksekusi sebuah fungsi.

    Args:
        func: Fungsi yang akan diukur waktunya.
        *args: Argument posisi untuk fungsi.
        **kwargs: Argument keyword untuk fungsi.

    Returns:
        Tuple berisi (hasil_fungsi, waktu_eksekusi_detik)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    waktu = round((end - start) * 1000, 2)  # Konversi ke milidetik
    return result, waktu


def cetak_pemisah(panjang: int = 50) -> None:
    """Cetak garis pemisah di terminal.

    Args:
        panjang: Panjang karakter pemisah.
    """
    print("=" * panjang)


def cetak_header(judul: str) -> None:
    """Cetak header dengan format rapi.

    Args:
        judul: Teks judul yang akan dicetak.
    """
    cetak_pemisah()
    print(f"{judul:^50}")
    cetak_pemisah()


def cetak_produk(produk: Dict[str, Any]) -> None:
    """Cetak satu produk dengan format rapi.

    Args:
        produk: Dictionary data produk.
    """
    print(f"ID        : {produk.get('_id', '-')}")
    print(f"Nama      : {produk.get('nama', '-')}")
    print(f"Kategori  : {produk.get('kategori', '-')}")
    print(f"Harga     : {format_harga(produk.get('harga', 0))}")
    print(f"Stok      : {produk.get('stok', 0)}")
    print(f"Spesifikasi: {produk.get('spesifikasi', '-')}")
    print("-" * 50)


def cetak_daftar_produk(produk_list: List[Dict[str, Any]]) -> None:
    """Cetak daftar produk.

    Args:
        produk_list: List dictionary data produk.
    """
    for produk in produk_list:
        cetak_produk(produk)


def cetak_hasil_pencarian(
    sumber: str,
    keyword: str,
    jumlah: int,
    produk_list: List[Dict[str, Any]],
    waktu: float
) -> None:
    """Cetak hasil pencarian dari suatu sumber.

    Args:
        sumber: Nama sumber (MongoDB / Elasticsearch).
        keyword: Keyword yang dicari.
        jumlah: Jumlah hasil.
        produk_list: List produk hasil pencarian.
        waktu: Waktu eksekusi dalam milidetik.
    """
    print(f"\n[Sumber: {sumber}]")
    print(f"Keyword  : '{keyword}'")
    print(f"Jumlah   : {jumlah} data ditemukan")
    print(f"Waktu    : {waktu} ms")
    print("-" * 50)

    if jumlah == 0:
        print("Tidak ada data ditemukan.")
    else:
        for i, produk in enumerate(produk_list, 1):
            print(f"{i}. {produk.get('nama', '-')} "
                  f"({produk.get('kategori', '-')}) - "
                  f"{format_harga(produk.get('harga', 0))}")

    print()


def input_pilihan(prompt: str, min_val: int, max_val: int) -> int:
    """Validasi input angka dari user.

    Args:
        prompt: Teks prompt yang ditampilkan.
        min_val: Nilai minimum yang diizinkan.
        max_val: Nilai maksimum yang diizinkan.

    Returns:
        Integer hasil input yang sudah divalidasi.
    """
    while True:
        try:
            pilihan = int(input(prompt).strip())
            if min_val <= pilihan <= max_val:
                return pilihan
            print(f"Pilihan harus antara {min_val}-{max_val}.")
        except ValueError:
            print("Input harus berupa angka valid.")


def input_text(prompt: str) -> str:
    """Ambil input teks dari user dengan validasi.

    Args:
        prompt: Teks prompt yang ditampilkan.

    Returns:
        String teks yang sudah di-strip.
    """
    teks = input(prompt).strip()
    if not teks:
        print("Input tidak boleh kosong.")
        return input_text(prompt)
    return teks