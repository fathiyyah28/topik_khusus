"""
Modul untuk operasi-operasi Redis.

Modul ini menyediakan fungsi-fungsi untuk:
- Menyimpan data mahasiswa (SET)
- Mengambil data mahasiswa (GET)
- Increment counter pengunjung (INCR)
- Melihat nilai counter (GET)
- Mengecek keberadaan key (EXISTS)
- Menghapus key (DELETE)
"""

from typing import Optional
import redis


# Key constants untuk menyimpan data di Redis
KEY_MAHASISWA = "mahasiswa:nama"
KEY_COUNTER = "counter:pengunjung"


def set_mahasiswa(client: redis.Redis, nama: str) -> bool:
    """
    Menyimpan nama mahasiswa ke Redis menggunakan perintah SET.

    Args:
        client: Objek koneksi Redis.
        nama: Nama mahasiswa yang akan disimpan.

    Returns:
        bool: True jika berhasil, False jika gagal.

    Example:
        >>> set_mahasiswa(client, "Budi")
        ✅ Data mahasiswa berhasil disimpan.
    """
    try:
        # Validasi input: nama tidak boleh kosong
        if not nama or not nama.strip():
            print("❌ Nama mahasiswa tidak boleh kosong.")
            return False

        # Simpan data ke Redis dengan perintah SET
        # Format: SET key value
        client.set(KEY_MAHASISWA, nama.strip())
        print(f"✅ Data mahasiswa '{nama.strip()}' berhasil disimpan.")
        return True

    except redis.RedisError as e:
        print(f"❌ Gagal menyimpan data ke Redis: {e}")
        return False

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False


def get_mahasiswa(client: redis.Redis) -> Optional[str]:
    """
    Mengambil nama mahasiswa dari Redis menggunakan perintah GET.

    Args:
        client: Objek koneksi Redis.

    Returns:
        Optional[str]: Nama mahasiswa jika ditemukan, None jika tidak ada.

    Example:
        >>> nama = get_mahasiswa(client)
        >>> if nama:
        ...     print(f"Nama: {nama}")
    """
    try:
        # Cek apakah key mahasiswa ada di Redis
        if not client.exists(KEY_MAHASISWA):
            print("📭 Belum ada data mahasiswa yang tersimpan.")
            return None

        # Ambil data dari Redis dengan perintah GET
        # Format: GET key
        nama = client.get(KEY_MAHASISWA)

        if nama:
            print(f"📋 Nama Mahasiswa: {nama}")
        else:
            print("📭 Data mahasiswa kosong.")

        return nama

    except redis.RedisError as e:
        print(f"❌ Gagal mengambil data dari Redis: {e}")
        return None

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return None


def increment_counter(client: redis.Redis) -> Optional[int]:
    """
    Menambah counter pengunjung menggunakan perintah INCR.

    Args:
        client: Objek koneksi Redis.

    Returns:
        Optional[int]: Nilai counter setelah increment, None jika gagal.

    Example:
        >>> counter = increment_counter(client)
        >>> print(f"Counter: {counter}")
    """
    try:
        # Increment counter dengan perintah INCR
        # Format: INCR key
        # Jika key belum ada, Redis akan membuatnya dengan nilai 0 lalu increment
        counter = client.incr(KEY_COUNTER)
        print(f"🔄 Counter pengunjung bertambah menjadi: {counter}")
        return counter

    except redis.RedisError as e:
        print(f"❌ Gagal increment counter: {e}")
        return None

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return None


def get_counter(client: redis.Redis) -> Optional[int]:
    """
    Melihat nilai counter pengunjung saat ini.

    Args:
        client: Objek koneksi Redis.

    Returns:
        Optional[int]: Nilai counter saat ini, None jika gagal.

    Example:
        >>> counter = get_counter(client)
        >>> if counter is not None:
        ...     print(f"Counter: {counter}")
    """
    try:
        # Cek apakah key counter ada di Redis
        if not client.exists(KEY_COUNTER):
            print("📭 Counter belum pernah di-increment.")
            return 0

        # Ambil nilai counter dengan perintah GET
        nilai_counter = client.get(KEY_COUNTER)

        if nilai_counter is not None:
            print(f"📊 Nilai Counter Saat Ini: {nilai_counter}")
            return int(nilai_counter)
        else:
            print("📭 Counter kosong.")
            return 0

    except redis.RedisError as e:
        print(f"❌ Gagal mengambil counter: {e}")
        return None

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return None


def delete_mahasiswa(client: redis.Redis) -> bool:
    """
    Menghapus data mahasiswa dari Redis menggunakan perintah DEL.

    Args:
        client: Objek koneksi Redis.

    Returns:
        bool: True jika berhasil menghapus, False jika gagal.

    Example:
        >>> delete_mahasiswa(client)
        ✅ Data mahasiswa berhasil dihapus.
    """
    try:
        # Cek apakah data mahasiswa ada
        if not client.exists(KEY_MAHASISWA):
            print("📭 Tidak ada data mahasiswa untuk dihapus.")
            return False

        # Hapus data dengan perintah DELETE
        # Format: DEL key
        client.delete(KEY_MAHASISWA)
        print("✅ Data mahasiswa berhasil dihapus.")
        return True

    except redis.RedisError as e:
        print(f"❌ Gagal menghapus data: {e}")
        return False

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False


def check_connection(client: Optional[redis.Redis]) -> bool:
    """
    Mengecek apakah koneksi Redis masih aktif.

    Args:
        client: Objek koneksi Redis yang akan dicek.

    Returns:
        bool: True jika koneksi aktif, False jika tidak.
    """
    if client is None:
        print("❌ Koneksi Redis tidak tersedia.")
        return False

    try:
        # Ping Redis untuk cek koneksi
        client.ping()
        return True

    except (redis.ConnectionError, redis.TimeoutError) as e:
        print(f"❌ Koneksi Redis terputus: {e}")
        return False

    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return False