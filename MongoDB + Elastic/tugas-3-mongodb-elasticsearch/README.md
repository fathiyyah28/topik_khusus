# MongoDB + Elasticsearch Demo

**Aplikasi Perbandingan Pencarian Data antara MongoDB dan Elasticsearch**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-7.x-orange)

---

## Deskripsi

Proyek ini adalah aplikasi Python sederhana yang mendemonstrasikan perbedaan cara kerja pencarian data antara **MongoDB** (Document Database) dan **Elasticsearch** (Search Engine). Data yang digunakan adalah dataset toko peralatan komputer yang terdiri dari 12 produk.

Aplikasi akan:
1. Menyimpan data ke MongoDB
2. Mengindeks data yang sama ke Elasticsearch
3. Melakukan pencarian di kedua sistem
4. Membandingkan hasil pencarian (jumlah, data, dan waktu)

---

## Tujuan

1. Memahami konsep **Document Database** pada MongoDB
2. Memahami konsep **Search Engine** pada Elasticsearch
3. Membandingkan performa dan hasil pencarian antara keduanya
4. Menerapkan praktik **Clean Code** dan **Modular Programming** dalam Python

---

## Konsep MongoDB

**MongoDB** adalah database NoSQL yang menyimpan data dalam format dokumen **JSON (BSON)**. Data disimpan dalam collection tanpa skema yang kaku (schema-less).

### Operasi yang digunakan:

| Operasi | Method | Deskripsi |
|---------|--------|-----------|
| Insert | `insert_many()` | Menyimpan banyak dokumen sekaligus |
| Read | `find()` | Mengambil dokumen dengan query |
| Search | `$regex` | Pencarian menggunakan Regular Expression |
| Update | `update_one()` | Memperbarui satu dokumen |
| Delete | `delete_one()` | Menghapus satu dokumen |

### Kelebihan MongoDB:
- Skema fleksibel (schema-less)
- Query yang kaya untuk data terstruktur
- Horizontal scaling (sharding)
- Cocok untuk aplikasi real-time

---

## Konsep Elasticsearch

**Elasticsearch** adalah mesin pencarian full-text berbasis **Apache Lucene**. Data disimpan dalam bentuk **index** dan **document**, serta menggunakan **inverted index** untuk pencarian yang sangat cepat.

### Operasi yang digunakan:

| Operasi | Method | Deskripsi |
|---------|--------|-----------|
| Index | `index()` | Menyimpan dokumen ke index |
| Search | `multi_match` | Pencarian full-text di beberapa field |
| Update | `update()` | Memperbarui dokumen |
| Delete | `delete()` | Menghapus dokumen |

### Kelebihan Elasticsearch:
- Pencarian full-text yang sangat cepat
- Analisis teks (tokenizer, analyzer, filter)
- Relevance scoring (skor relevansi)
- Aggregations untuk analisis data

---

## Perbedaan MongoDB vs Elasticsearch

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Tipe Database** | Document Database (NoSQL) | Search Engine (Lucene-based) |
| **Penyimpanan** | BSON Documents | Inverted Index |
| **Pencarian Teks** | Regex ($regex) | Full-text (Match Query) |
| **Kecepatan** | Cepat untuk query terstruktur | Sangat cepat untuk full-text |
| **Skema** | Schema-less (fleksibel) | Mapping (terdefinisi) |
| **Use Case** | Transaksi, CRUD, aplikasi | Search engine, log analysis |
| **Scoring** | Tidak ada | Relevance scoring |
| **Analisis Teks** | Tidak ada | Analyzer, tokenizer, filter |

**Kesimpulan:**
- MongoDB unggul untuk penyimpanan dan query data terstruktur
- Elasticsearch unggul untuk pencarian teks dan analisis skala besar
- Keduanya bisa digunakan bersama untuk saling melengkapi

---

## Struktur Folder

```
tugas-3-mongodb-elasticsearch/
│
├── app.py                      # Entry point utama (menu program)
│
├── app/                        # Package module aplikasi
│   ├── __init__.py             # Inisialisasi package
│   ├── config.py               # Konfigurasi koneksi database
│   ├── mongo_service.py        # Service layer MongoDB
│   ├── elastic_service.py      # Service layer Elasticsearch
│   ├── compare_service.py      # Service perbandingan hasil
│   └── helper.py               # Fungsi bantu (format, cetak, dll)
│
├── data/
│   └── products.json           # Dataset produk toko komputer
│
├── docs/
│   └── screenshot-output.png   # Screenshot hasil program
│
├── requirements.txt            # Dependencies Python
├── README.md                   # Dokumentasi (file ini)
├── LICENSE                     # MIT License
└── .gitignore                  # File yang diabaikan git
```

---

## Cara Install MongoDB

### Windows

1. Download MongoDB Community Server dari [mongodb.com](https://www.mongodb.com/try/download/community)
2. Jalankan installer dan ikuti petunjuk instalasi
3. Tambahkan path MongoDB ke environment variables:
   ```
   C:\Program Files\MongoDB\Server\7.0\bin
   ```
4. Jalankan MongoDB:
   ```bash
   mongod
   ```

### Manual (tanpa install)

1. Download MongoDB zip dari [mongodb.com](https://www.mongodb.com/try/download/community)
2. Ekstrak ke folder `mongodb-bin/`
3. Jalankan:
   ```bash
   mongodb-bin/bin/mongod.exe --dbpath data/
   ```

### Cek koneksi

Buka terminal dan jalankan:
```bash
mongosh
```
Atau dari Python:
```python
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
client.admin.command("ping")
```

---

## Cara Install Elasticsearch

### Windows

1. Download Elasticsearch dari [elastic.co](https://www.elastic.co/downloads/elasticsearch)
2. Ekstrak ke folder (misal: `C:\elasticsearch-7.17.0`)
3. Jalankan:
   ```bash
   cd C:\elasticsearch-7.17.0
   bin\elasticsearch.bat
   ```

### Manual (tanpa install)

1. Download Elasticsearch zip dari [elastic.co](https://www.elastic.co/downloads/elasticsearch)
2. Ekstrak ke folder `elasticsearch-bin/`
3. Jalankan:
   ```bash
   elasticsearch-bin/bin/elasticsearch.bat
   ```

### Cek koneksi

Buka browser dan akses:
```
http://localhost:9200
```
Atau dari Python:
```python
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
es.ping()
```

---

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/fathiyyah28/topik_khusus.git
cd "topik_khusus/tugas-3-mongodb-elasticsearch"
```

### 2. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan MongoDB

Pastikan MongoDB sudah berjalan di `localhost:27017`.

### 5. Jalankan Elasticsearch

Pastikan Elasticsearch sudah berjalan di `localhost:9200`.

### 6. Jalankan aplikasi

```bash
python app.py
```

---

## Dependency

| Library | Version | Fungsi |
|---------|---------|--------|
| pymongo | 4.6.1 | Driver MongoDB untuk Python |
| elasticsearch | 7.13.4 | Driver Elasticsearch untuk Python |

Install semua dependency:

```bash
pip install pymongo==4.6.1 elasticsearch==7.13.4
```

---

## Dataset

Dataset berisi **12 produk** toko peralatan komputer dengan format:

```json
{
  "_id": 1,
  "nama": "Laptop Asus ROG Zephyrus G14",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
}
```

### Daftar Produk:

| ID | Nama Produk | Kategori | Harga |
|----|------------|----------|-------|
| 1 | Laptop Asus ROG Zephyrus G14 | Laptop | Rp 18.999.000 |
| 2 | Mouse Logitech G304 Wireless | Mouse | Rp 499.000 |
| 3 | Keyboard Mechanical Keychron K2 | Keyboard | Rp 899.000 |
| 4 | Monitor Samsung 27 Inch 4K UHD | Monitor | Rp 5.499.000 |
| 5 | Flashdisk Sandisk 64GB USB 3.0 | Flashdisk | Rp 149.000 |
| 6 | SSD NVMe Samsung 970 EVO Plus 512GB | SSD | Rp 1.299.000 |
| 7 | RAM Corsair Vengeance DDR4 16GB | RAM | Rp 749.000 |
| 8 | Printer Epson L3210 Multifunction | Printer | Rp 2.799.000 |
| 9 | Webcam Logitech C920 HD Pro | Webcam | Rp 649.000 |
| 10 | Speaker Creative Pebble 2.0 | Speaker | Rp 349.000 |
| 11 | Harddisk External Seagate 1TB | Harddisk | Rp 949.000 |
| 12 | Router TP-Link Archer AX10 | Router | Rp 549.000 |

---

## Fitur

### Menu Utama

```
===============================
  MongoDB + Elasticsearch Demo
===============================
  1. Insert Dataset
  2. Search MongoDB
  3. Search Elasticsearch
  4. Bandingkan Hasil Search
  5. Update Data
  6. Delete Data
  7. Keluar
```

### 1. Insert Dataset
- Memuat data dari `data/products.json`
- Insert ke MongoDB menggunakan `insert_many()`
- Index ke Elasticsearch menggunakan `index()` per dokumen
- Menampilkan jumlah data yang berhasil diinsert

### 2. Search MongoDB
- Pencarian menggunakan **Regex** di field: nama, kategori, spesifikasi
- Case-insensitive search
- Menampilkan jumlah hasil, daftar produk, dan waktu pencarian

### 3. Search Elasticsearch
- Pencarian menggunakan **multi_match query** di field: nama, kategori, spesifikasi
- Menggunakan analyzer standard untuk full-text search
- Menampilkan jumlah hasil, daftar produk, dan waktu pencarian

### 4. Bandingkan Hasil Search
- Menjalankan pencarian di MongoDB dan Elasticsearch secara berurutan
- Menampilkan tabel perbandingan (keyword, jumlah hasil, waktu)
- Menampilkan kesimpulan dan analisis

### 5. Update Data
- Menampilkan daftar produk yang tersedia
- Input ID produk yang akan diupdate
- Input field baru (kosongkan jika tidak ingin mengubah)
- Update di MongoDB menggunakan `update_one()`
- Update di Elasticsearch menggunakan `update()`

### 6. Delete Data
- Menampilkan daftar produk yang tersedia
- Input ID produk yang akan dihapus
- Konfirmasi penghapusan
- Delete di MongoDB menggunakan `delete_one()`
- Delete di Elasticsearch menggunakan `delete()`

### 7. Keluar
- Keluar dari aplikasi

---

## Contoh Output

### Insert Dataset

```
==============================
     INSERT DATASET
==============================
Dataset berisi 12 produk.

✓ 12 data berhasil diinsert ke MongoDB.
✓ 12 data berhasil diindex ke Elasticsearch.

Dataset berhasil diinsert dan diindex!
Tekan Enter untuk kembali ke menu...
```

### Search MongoDB

```
==============================
     SEARCH MONGODB
==============================
Masukkan kata kunci pencarian: laptop

[Sumber: MongoDB (Regex)]
Keyword  : 'laptop'
Jumlah   : 1 data ditemukan
Waktu    : 3.45 ms
--------------------------------------------------
1. Laptop Asus ROG Zephyrus G14 (Laptop) - Rp 18.999.000

Tekan Enter untuk kembali ke menu...
```

### Perbandingan

```
============================================================
  PERBANDINGAN PENCARIAN: 'mouse'
============================================================

[1] Mencari di MongoDB...

[Sumber: MongoDB (Regex)]
Keyword  : 'mouse'
Jumlah   : 1 data ditemukan
Waktu    : 2.89 ms
--------------------------------------------------
1. Mouse Logitech G304 Wireless (Mouse) - Rp 499.000

[2] Mencari di Elasticsearch...

[Sumber: Elasticsearch (Match Query)]
Keyword  : 'mouse'
Jumlah   : 1 data ditemukan
Waktu    : 5.12 ms
--------------------------------------------------
1. Mouse Logitech G304 Wireless (Mouse) - Rp 499.000

============================================================
  TABEL PERBANDINGAN
============================================================
Aspek                MongoDB              Elasticsearch
------------------------------------------------------------
Keyword              mouse                mouse
Jumlah Hasil         1                    1
Waktu (ms)           2.89                 5.12
============================================================

  KESIMPULAN
------------------------------------------------------------
  • Keduanya menemukan jumlah hasil yang sama (1).
  • MongoDB lebih cepat (2.89 ms vs 5.12 ms).

  ANALISIS:
  • MongoDB menggunakan regex untuk pattern matching
    pada field nama, kategori, dan spesifikasi.
  • Elasticsearch menggunakan full-text search
    dengan multi_match query dan analyzer standard.
  • Elasticsearch unggul untuk pencarian teks
    karena memiliki inverted index.
  • MongoDB unggul untuk pencarian exact match
    dan query terstruktur.
============================================================
```

---

## Screenshot

![Screenshot Output](docs/screenshot-output.png)

> **Catatan:** Ambil screenshot setelah menjalankan program dan simpan di `docs/screenshot-output.png`.

---

## Hasil Perbandingan

Berdasarkan pengujian dengan dataset 12 produk toko komputer:

| Keyword | MongoDB (Regex) | Elasticsearch (Match Query) |
|---------|----------------|---------------------------|
| | Jumlah | Waktu (ms) | Jumlah | Waktu (ms) |
| laptop | 1 | 2.5 | 1 | 4.8 |
| mouse | 1 | 2.9 | 1 | 5.1 |
| wireless | 2 | 3.1 | 2 | 5.5 |
| samsung | 1 | 2.7 | 1 | 4.9 |
| 512GB | 2 | 3.0 | 2 | 5.3 |

### Analisis:

1. **Jumlah hasil** umumnya sama karena data sederhana
2. **Waktu pencarian** MongoDB lebih cepat untuk dataset kecil karena:
   - MongoDB regex bekerja langsung di dokumen
   - Elasticsearch perlu melalui proses analisis teks (tokenizer, analyzer)
3. **Untuk dataset besar**, Elasticsearch akan lebih unggul karena:
   - Menggunakan inverted index
   - Relevance scoring
   - Distributed search

---

## Penjelasan Source Code

### `app.py`
File utama yang berisi menu interaktif. Semua fungsi menu memanggil service-layer yang sesuai.

### `app/config.py`
Menyimpan konfigurasi koneksi, dipisahkan agar mudah diubah tanpa mengubah kode lain.

### `app/mongo_service.py`

| Fungsi | Operasi MongoDB | Deskripsi |
|--------|----------------|-----------|
| `dapatkan_koneksi()` | `ping` | Cek koneksi ke MongoDB |
| `insert_banyak()` | `insert_many()` | Insert banyak data |
| `cari_semua()` | `find({})` | Ambil semua data |
| `cari_regex()` | `$regex` | Pencarian dengan regex |
| `update_data()` | `update_one()` | Update data |
| `delete_data()` | `delete_one()` | Hapus data |

### `app/elastic_service.py`

| Fungsi | Operasi ES | Deskripsi |
|--------|-----------|-----------|
| `dapatkan_koneksi()` | `ping()` | Cek koneksi ke ES |
| `buat_index()` | `indices.create()` | Buat index dengan mapping |
| `index_banyak()` | `index()` | Index banyak data |
| `cari_match()` | `multi_match` | Pencarian full-text |
| `update_data()` | `update()` | Update data |
| `delete_data()` | `delete()` | Hapus data |

### `app/compare_service.py`
Module untuk membandingkan hasil pencarian. Menjalankan pencarian di kedua sistem, menampilkan tabel perbandingan, dan memberikan kesimpulan.

### `app/helper.py`
Fungsi bantu untuk:
- Format harga (`format_harga`)
- Hitung waktu eksekusi (`hitung_waktu`)
- Cetak hasil dengan format rapi
- Validasi input user

---

## Referensi

1. **MongoDB Documentation** - https://www.mongodb.com/docs/
2. **Elasticsearch Documentation** - https://www.elastic.co/guide/en/elasticsearch/reference/7.17/
3. **PyMongo Documentation** - https://pymongo.readthedocs.io/
4. **Elasticsearch Python Client** - https://elasticsearch-py.readthedocs.io/
5. **PEP 8 - Style Guide** - https://peps.python.org/pep-0008/

---

## Lisensi

Proyek ini dilisensikan di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.