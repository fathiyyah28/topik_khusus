"""
Program Utama - Redis Python Demo.

Program ini adalah aplikasi terminal interaktif untuk mendemonstrasikan
penggunaan Redis sebagai database key-value menggunakan Python.

Fitur:
1. Simpan Nama Mahasiswa (SET)
2. Lihat Nama Mahasiswa (GET)
3. Tambah Counter Pengunjung (INCR)
4. Lihat Counter (GET)
5. Keluar
"""

import sys
from typing import Optional
import redis
from app.redis_client import create_connection
from app.redis_service import (
    set_mahasiswa,
    get_mahasiswa,
    increment_counter,
    get_counter,
    check_connection,
)


def clear_screen() -> None:
    """Membersihkan layar terminal."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def display_header() -> None:
    """Menampilkan header aplikasi."""
    print("=" * 55)
    print("          REDIS PYTHON DEMO")
    print("    Demonstrasi Redis Key-Value Database")
    print("=" * 55)
    print()


def display_menu() -> None:
    """Menampilkan menu utama aplikasi."""
    print("Menu:")
    print("-" * 55)
    print("  1. Simpan Nama Mahasiswa  (SET)")
    print("  2. Lihat Nama Mahasiswa   (GET)")
    print("  3. Tambah Counter         (INCR)")
    print("  4. Lihat Counter          (GET)")
    print("  5. Keluar")
    print("-" * 55)


def get_user_choice() -> int:
    """
    Mendapatkan pilihan menu dari user.

    Returns:
        int: Nomor menu yang dipilih (1-5).

    Example:
        >>> pilihan = get_user_choice()
        Masukkan pilihan [1-5]: 1
    """
    while True:
        try:
            pilihan = input("Masukkan pilihan [1-5]: ").strip()

            # Validasi input: harus angka
            if not pilihan.isdigit():
                print("❌ Input harus berupa angka.")
                continue

            pilihan = int(pilihan)

            # Validasi input: harus dalam range 1-5
            if pilihan < 1 or pilihan > 5:
                print("❌ Pilihan harus antara 1-5.")
                continue

            return pilihan

        except ValueError:
            print("❌ Input tidak valid. Masukkan angka 1-5.")

        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh user.")
            sys.exit(0)


def handle_set_mahasiswa(client: redis.Redis) -> None:
    """
    Menangani menu 1: Menyimpan nama mahasiswa.

    Args:
        client: Objek koneksi Redis.
    """
    print("\n--- Simpan Nama Mahasiswa ---")
    nama = input("Masukkan nama mahasiswa: ").strip()

    if not nama:
        print("❌ Nama tidak boleh kosong.")
        return

    set_mahasiswa(client, nama)


def handle_get_mahasiswa(client: redis.Redis) -> None:
    """
    Menangani menu 2: Melihat nama mahasiswa.

    Args:
        client: Objek koneksi Redis.
    """
    print("\n--- Lihat Nama Mahasiswa ---")
    get_mahasiswa(client)


def handle_increment_counter(client: redis.Redis) -> None:
    """
    Menangani menu 3: Increment counter pengunjung.

    Args:
        client: Objek koneksi Redis.
    """
    print("\n--- Tambah Counter Pengunjung ---")
    increment_counter(client)


def handle_get_counter(client: redis.Redis) -> None:
    """
    Menangani menu 4: Melihat nilai counter.

    Args:
        client: Objek koneksi Redis.
    """
    print("\n--- Lihat Counter ---")
    get_counter(client)


def handle_menu_choice(client: redis.Redis, pilihan: int) -> bool:
    """
    Memproses pilihan menu yang dipilih user.

    Args:
        client: Objek koneksi Redis.
        pilihan: Nomor menu yang dipilih (1-5).

    Returns:
        bool: True jika program harus dilanjutkan, False jika keluar.

    Raises:
        ValueError: Jika pilihan tidak valid.
    """
    # Mapping pilihan menu ke fungsi handler
    menu_handlers = {
        1: handle_set_mahasiswa,
        2: handle_get_mahasiswa,
        3: handle_increment_counter,
        4: handle_get_counter,
    }

    if pilihan == 5:
        print("\nTerima kasih telah menggunakan Redis Python Demo!")
        return False

    if pilihan in menu_handlers:
        # Cek koneksi Redis sebelum setiap operasi
        if not check_connection(client):
            print("Koneksi Redis terputus. Program akan keluar.")
            return False

        # Jalankan handler sesuai pilihan menu
        menu_handlers[pilihan](client)
        return True

    # Seharusnya tidak sampai di sini karena sudah divalidasi
    raise ValueError(f"Pilihan tidak valid: {pilihan}")


def main() -> None:
    """
    Fungsi utama program.

    Fungsi ini mengatur alur program:
    1. Membuat koneksi ke Redis
    2. Jika gagal, program berhenti
    3. Jika berhasil, tampilkan menu dan proses input user
    4. Loop sampai user memilih keluar
    """
    # Header program
    clear_screen()
    display_header()

    print("Menghubungkan ke Redis...")
    client = create_connection()

    # Jika koneksi gagal, hentikan program
    if client is None:
        print("\nProgram tidak dapat berjalan tanpa koneksi Redis.")
        print("Silakan jalankan redis-server terlebih dahulu.")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)

    print("\nSelamat datang di Redis Python Demo!")
    input("Tekan Enter untuk melanjutkan...")

    # Loop utama program
    while True:
        try:
            clear_screen()
            display_header()
            display_menu()

            pilihan = get_user_choice()
            lanjutkan = handle_menu_choice(client, pilihan)

            if not lanjutkan:
                break

            print("\n" + "-" * 55)
            input("Tekan Enter untuk kembali ke menu...")

        except KeyboardInterrupt:
            print("\n\nProgram dihentikan oleh user.")
            break

        except Exception as e:
            print(f"\n❌ Terjadi error: {e}")
            input("\nTekan Enter untuk melanjutkan...")

    print("\nSampai jumpa!")


# Entry point program
if __name__ == "__main__":
    main()