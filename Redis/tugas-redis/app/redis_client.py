"""
Modul untuk konfigurasi dan koneksi ke Redis.

Modul ini bertanggung jawab untuk:
- Membuat koneksi ke Redis server
- Mengecek status koneksi dengan ping
- Memberikan error handling jika Redis tidak berjalan
"""

import redis
from typing import Optional


def create_connection(
    host: str = "localhost",
    port: int = 6380,
    db: int = 0,
    decode_responses: bool = True,
    socket_timeout: int = 5,
) -> Optional[redis.Redis]:
    """
    Membuat dan mengembalikan koneksi ke Redis server.

    Args:
        host: Alamat host Redis server (default: localhost).
        port: Port Redis server (default: 6379).
        db: Nomor database Redis (default: 0).
        decode_responses: Jika True, response akan berupa string (default: True).
        socket_timeout: Timeout koneksi dalam detik (default: 5).

    Returns:
        Optional[redis.Redis]: Objek koneksi Redis jika berhasil,
                               None jika gagal.

    Example:
        >>> client = create_connection()
        >>> if client:
        ...     print("Koneksi berhasil")
    """
    try:
        # Buat objek koneksi Redis dengan parameter yang diberikan
        client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            socket_timeout=socket_timeout,
        )

        # Cek koneksi dengan ping ke Redis server
        client.ping()
        print(f"✅ Berhasil terhubung ke Redis ({host}:{port})")
        return client

    except redis.ConnectionError:
        print("=" * 50)
        print("❌ Gagal terhubung ke Redis.")
        print("   Pastikan redis-server.exe sedang berjalan.")
        print("   Jalankan: redis-server")
        print("=" * 50)
        return None

    except redis.TimeoutError:
        print("=" * 50)
        print("❌ Koneksi ke Redis timeout.")
        print("   Periksa apakah Redis server merespon.")
        print("=" * 50)
        return None

    except Exception as e:
        print(f"❌ Error tidak terduga saat koneksi ke Redis: {e}")
        return None