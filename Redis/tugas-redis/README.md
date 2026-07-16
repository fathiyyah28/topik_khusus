# 🚀 Redis Python Demo

**Aplikasi Demonstrasi Redis Key-Value Database Menggunakan Python**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Redis](https://img.shields.io/badge/Redis-7.0%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Daftar Isi

- [Deskripsi](#deskripsi)
- [Tujuan](#tujuan)
- [Teknologi](#teknologi)
- [Struktur Folder](#struktur-folder)
- [Fitur](#fitur)
- [Cara Install](#cara-install)
- [Cara Menjalankan Redis](#cara-menjalankan-redis)
- [Cara Menjalankan Program](#cara-menjalankan-program)
- [Dependency](#dependency)
- [Contoh Output](#contoh-output)
- [Screenshot](#screenshot)
- [Penjelasan Source Code](#penjelasan-source-code)
- [Cara Push ke GitHub](#cara-push-ke-github)
- [Referensi](#referensi)
- [Lisensi](#lisensi)

---

## 📖 Deskripsi

**Redis Python Demo** adalah aplikasi terminal interaktif berbasis Python yang mendemonstrasikan penggunaan **Redis** sebagai database **Key-Value**. Program ini dibuat sebagai tugas mata kuliah **Topik Khusus** untuk menunjukkan pemahaman tentang:

- Konsep database NoSQL (Key-Value Store)
- Operasi dasar Redis (SET, GET, INCR, EXISTS, DELETE)
- Integrasi Redis dengan Python menggunakan library `redis-py`
- Praktik pemrograman Python yang baik (clean code, error handling, modular)

---

## 🎯 Tujuan

1. Memahami konsep **Redis** sebagai in-memory data store
2. Mampu mengintegrasikan **Python** dengan **Redis**
3. Mengimplementasikan operasi **CRUD** sederhana menggunakan Redis
4. Menerapkan **clean code** dan **error handling** dalam Python
5. Membuat dokumentasi project yang profesional

---

## 🛠 Teknologi

| Teknologi | Versi | Deskripsi |
|-----------|-------|-----------|
| **Python** | 3.8+ | Bahasa pemrograman utama |
| **Redis** | 7.0+ | In-memory key-value database |
| **redis-py** | 5.0+ | Library Python untuk Redis |

---

## 📁 Struktur Folder

```
tugas-redis/
│
├── app/                          # Package aplikasi
│   ├── __init__.py               # Inisialisasi package
│   ├── redis_client.py           # Konfigurasi koneksi Redis
│   └── redis_service.py          # Operasi-operasi Redis
│
├── docs/                         # Dokumentasi
│   └── screenshot-output.png     # Screenshot output program
│
├── redis_app.py                  # Program utama (entry point)
├── requirements.txt              # Daftar dependency
├── README.md                     # Dokumentasi project (file ini)
├── .gitignore                    # File yang diabaikan Git
└── LICENSE                       # Lisensi MIT
```

### Penjelasan Setiap File

| File | Fungsi |
|------|--------|
| `app/__init__.py` | Menandai folder `app` sebagai Python package |
| `app/redis_client.py` | Membuat dan mengelola koneksi ke Redis server |
| `app/redis_service.py` | Berisi fungsi-fungsi operasi Redis (SET, GET, INCR, dll) |
| `redis_app.py` | Program utama dengan menu interaktif |
| `requirements.txt` | Daftar library yang dibutuhkan |
| `README.md` | Dokumentasi lengkap project |
| `.gitignore` | Konfigurasi file yang diabaikan Git |
| `LICENSE` | Lisensi MIT untuk project |

---

## ✨ Fitur

Program ini memiliki **5 menu utama** yang mendemonstrasikan operasi Redis:

| No | Menu | Operasi Redis | Deskripsi |
|----|------|---------------|-----------|
| 1 | Simpan Nama Mahasiswa | **SET** | Menyimpan data nama mahasiswa ke Redis |
| 2 | Lihat Nama Mahasiswa | **GET** + **EXISTS** | Mengambil dan menampilkan data mahasiswa |
| 3 | Tambah Counter Pengunjung | **INCR** | Menambah counter pengunjung (auto-increment) |
| 4 | Lihat Counter | **GET** + **EXISTS** | Melihat nilai counter saat ini |
| 5 | Keluar | - | Keluar dari program |

### Fitur Tambahan
- ✅ **Error Handling** — Menangani error koneksi, input tidak valid, dll
- ✅ **Validasi Input** — Memastikan input user sesuai format
- ✅ **Pengecekan Koneksi** — Mengecek koneksi Redis sebelum setiap operasi
- ✅ **Clean Code** — Mengikuti PEP8, menggunakan fungsi modular, docstring
- ✅ **User Friendly** — Tampilan menu yang rapi dengan emoji indikator

---

## 📦 Cara Install

### Prasyarat

1. **Python 3.8+** sudah terinstall di sistem
2. **Redis Server** sudah terinstall (lihat [Cara Menjalankan Redis](#cara-menjalankan-redis))
3. **Git** sudah terinstall (untuk version control)

### Langkah-langkah

1. **Clone repository** (atau download ZIP):
   ```bash
   git clone https://github.com/fathiyyah28/topik_khusus.git
   cd topik_khusus/tugas-redis
   ```

2. **Buat virtual environment** (disarankan):
   ```bash
   python -m venv venv
   ```

3. **Aktifkan virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependency**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Cara Menjalankan Redis

### Windows

1. Buka folder tempat Redis diinstall (biasanya `C:\Program Files\Redis\` atau folder project ini)
2. Jalankan **redis-server.exe**:
   ```bash
   redis-server.exe
   ```
   Atau double-click `redis-server.exe` di File Explorer

3. Biarkan terminal Redis tetap terbuka (server berjalan di background)

### Linux/Mac

```bash
# Install Redis (jika belum)
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # MacOS

# Jalankan Redis
redis-server
```

### Verifikasi Redis Berjalan

Buka terminal baru dan jalankan:
```bash
redis-cli ping
```
Jika Redis berjalan, akan muncul response: `PONG`

---

## ▶️ Cara Menjalankan Program

1. **Pastikan Redis Server sudah berjalan** (lihat langkah sebelumnya)

2. **Buka terminal** di folder `tugas-redis/`

3. **Jalankan program**:
   ```bash
   python redis_app.py
   ```

4. **Ikuti menu interaktif** yang muncul di terminal

---

## 📚 Dependency

Library yang dibutuhkan (tercantum di `requirements.txt`):

```
redis>=5.0.0
```

Library `redis` adalah **redis-py** — Python client resmi untuk Redis.

---

## 💻 Contoh Output

### Saat Program Pertama Kali Dijalankan

```
=======================================================
          REDIS PYTHON DEMO
    Demonstrasi Redis Key-Value Database
=======================================================

Menghubungkan ke Redis...
✅ Berhasil terhubung ke Redis (localhost:6379)

Selamat datang di Redis Python Demo!
Tekan Enter untuk melanjutkan...
```

### Menu Utama

```
=======================================================
          REDIS PYTHON DEMO
    Demonstrasi Redis Key-Value Database
=======================================================

Menu:
-------------------------------------------------------
  1. Simpan Nama Mahasiswa  (SET)
  2. Lihat Nama Mahasiswa   (GET)
  3. Tambah Counter         (INCR)
  4. Lihat Counter          (GET)
  5. Keluar
-------------------------------------------------------
Masukkan pilihan [1-5]:
```

### Menyimpan Data Mahasiswa

```
--- Simpan Nama Mahasiswa ---
Masukkan nama mahasiswa: Fathiyyah
✅ Data mahasiswa 'Fathiyyah' berhasil disimpan.
```

### Melihat Data Mahasiswa

```
--- Lihat Nama Mahasiswa ---
📋 Nama Mahasiswa: Fathiyyah
```

### Increment Counter

```
--- Tambah Counter Pengunjung ---
🔄 Counter pengunjung bertambah menjadi: 1
```

### Melihat Counter

```
--- Lihat Counter ---
📊 Nilai Counter Saat Ini: 1
```

### Error Handling (Redis Tidak Berjalan)

```
=======================================================
          REDIS PYTHON DEMO
    Demonstrasi Redis Key-Value Database
=======================================================

Menghubungkan ke Redis...
======================================================
❌ Gagal terhubung ke Redis.
   Pastikan redis-server.exe sedang berjalan.
   Jalankan: redis-server
======================================================

Program tidak dapat berjalan tanpa koneksi Redis.
Silakan jalankan redis-server terlebih dahulu.

Tekan Enter untuk keluar...
```

---

## 📸 Screenshot

![Output Program](docs/screenshot-output.png)

*Screenshot akan ditambahkan setelah program dijalankan.*

---

## 📝 Penjelasan Source Code

### 1. `app/redis_client.py` — Koneksi Redis

File ini bertanggung jawab untuk membuat koneksi ke Redis server.

```python
def create_connection(host="localhost", port=6379, ...):
    """
    Membuat koneksi ke Redis server.
    - Menggunakan redis.Redis() untuk membuat objek koneksi
    - Menggunakan ping() untuk verifikasi koneksi
    - Mengembalikan None jika gagal (dengan pesan error)
    """
```

**Konsep Penting:**
- **redis.Redis()** — Membuat objek koneksi ke Redis
- **ping()** — Mengecek apakah server Redis merespon
- **ConnectionError** — Error jika Redis tidak berjalan
- **decode_responses=True** — Agar response berupa string, bukan bytes

### 2. `app/redis_service.py` — Operasi Redis

File ini berisi fungsi-fungsi untuk operasi Redis.

```python
# SET - Menyimpan data
def set_mahasiswa(client, nama):
    client.set("mahasiswa:nama", nama)

# GET - Mengambil data
def get_mahasiswa(client):
    nama = client.get("mahasiswa:nama")

# INCR - Increment counter
def increment_counter(client):
    counter = client.incr("counter:pengunjung")

# EXISTS - Cek keberadaan key
def check_exists(client, key):
    return client.exists(key)

# DELETE - Hapus data
def delete_mahasiswa(client):
    client.delete("mahasiswa:nama")
```

**Konsep Penting:**
- **Key-Value Store** — Data disimpan sebagai pasangan key-value
- **SET** — Menyimpan value dengan key tertentu
- **GET** — Mengambil value berdasarkan key
- **INCR** — Increment nilai integer secara atomik
- **EXISTS** — Mengecek apakah suatu key ada
- **DEL** — Menghapus key dan valuenya

### 3. `redis_app.py` — Program Utama

File ini adalah entry point program dengan menu interaktif.

```python
def main():
    """
    Alur program:
    1. Clear screen & tampilkan header
    2. Buat koneksi ke Redis
    3. Jika gagal -> tampilkan error & exit
    4. Jika berhasil -> loop menu sampai user pilih keluar
    """
```

**Konsep Penting:**
- **Modular Programming** — Setiap fungsi memiliki tanggung jawab spesifik
- **Error Handling** — try-except untuk menangani berbagai error
- **Input Validation** — Memastikan input user valid sebelum diproses
- **Menu-Driven** — Program berjalan berdasarkan pilihan user

---

## 🌐 Cara Push ke GitHub

Jika ingin mem-push project ke repository GitHub:

```bash
# 1. Inisialisasi Git
git init

# 2. Tambahkan semua file
git add .

# 3. Commit perubahan
git commit -m "Initial commit: Redis Python Demo"

# 4. Rename branch ke main
git branch -M main

# 5. Tambahkan remote repository
git remote add origin https://github.com/fathiyyah28/topik_khusus.git

# 6. Push ke GitHub
git push -u origin main
```

> **Catatan:** Jika repository sudah ada isinya, gunakan `git pull origin main --rebase` terlebih dahulu sebelum push.

---

## 📚 Referensi

- [Redis Documentation](https://redis.io/documentation) — Dokumentasi resmi Redis
- [redis-py Documentation](https://redis-py.readthedocs.io/) — Dokumentasi library redis-py
- [Python Redis Guide](https://realpython.com/python-redis/) — Tutorial Python + Redis dari Real Python
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) — Style Guide Python
- [Redis Commands](https://redis.io/commands) — Daftar lengkap perintah Redis

---

## 📄 Lisensi

Project ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---

<p align="center">
  Dibuat dengan ❤️ untuk Tugas Mata Kuliah Topik Khusus
  <br>
  <strong>Fathiyyah</strong> — 2026
</p>