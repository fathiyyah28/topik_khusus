# BAB 2: DESKRIPSI UMUM

## 2.1 Perspektif Produk

Mongo Search Portal adalah aplikasi berbasis microservice yang mendemonstrasikan perbandingan pencarian data antara MongoDB dan Elasticsearch. Aplikasi ini terdiri dari tiga komponen utama:

1. **Frontend Web (Vue.js 3)**: Antarmuka pengguna untuk mengelola produk dan melakukan pencarian.
2. **Core Service (FastAPI + MongoDB)**: Layanan backend untuk operasi CRUD data produk.
3. **Search Service (FastAPI + Elasticsearch)**: Layanan backend untuk full-text search.

Seluruh komponen berkomunikasi melalui REST API dan dijalankan dalam container Docker.

## 2.2 Fungsi Produk

Fungsi utama dari aplikasi ini adalah:

1. **Manajemen Produk**: Pengguna dapat menambah, melihat, mengubah, dan menghapus data produk.
2. **Pencarian Produk**: Pengguna dapat mencari produk menggunakan full-text search.
3. **Seed Data**: Pengguna dapat mengisi database dengan dataset contoh.
4. **Monitoring Status**: Pengguna dapat melihat status koneksi database dan service.
5. **Sinkronisasi Data**: Core Service secara otomatis menyinkronkan data ke Search Service.

## 2.3 Karakteristik Pengguna

| Karakteristik | Deskripsi |
|---------------|-----------|
| Target Pengguna | Mahasiswa, dosen, dan pengembang yang ingin mempelajari perbandingan MongoDB dan Elasticsearch |
| Tingkat Keahlian | Dasar hingga menengah dalam penggunaan aplikasi web |
| Kebutuhan Khusus | Tidak ada kebutuhan khusus; aplikasi menggunakan antarmuka web standar |

## 2.4 Batasan

1. Aplikasi tidak memiliki sistem autentikasi atau otorisasi pengguna.
2. Aplikasi hanya mendukung satu pengguna pada satu waktu.
3. Dataset terbatas pada 12 produk toko peralatan komputer.
4. Pencarian hanya mendukung satu kata kunci tanpa filter lanjutan.
5. Tidak ada fitur pagination pada daftar produk.
6. Aplikasi berjalan dalam lingkungan lokal (localhost).

## 2.5 Asumsi

1. Pengguna memiliki Docker Engine dan Docker Compose terinstal.
2. Sistem memiliki minimal 4GB RAM untuk menjalankan seluruh service.
3. Port 3000, 8001, 8002, 27017, dan 9200 tidak digunakan oleh aplikasi lain.
4. Koneksi internet tersedia untuk mengunduh image Docker.

## 2.6 Dependensi

### Perangkat Lunak

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Frontend | Vue.js | 3.4+ |
| Frontend | Vite | 5.0+ |
| Frontend | Bootstrap | 5.3+ |
| Backend (Core) | Python | 3.12 |
| Backend (Core) | FastAPI | 0.104+ |
| Backend (Search) | Python | 3.12 |
| Backend (Search) | FastAPI | 0.104+ |
| Database | MongoDB | 7 |
| Database | Elasticsearch | 8.15 |
| DevOps | Docker | 24+ |
| DevOps | Docker Compose | 2+ |

### Library Python (Core Service)

| Library | Versi | Kegunaan |
|---------|-------|----------|
| fastapi | 0.104.0 | Framework REST API |
| uvicorn | 0.24.0 | ASGI server |
| pymongo | 4.6.1 | MongoDB driver |
| pydantic | 2.5.0 | Data validation |
| httpx | 0.25.0 | HTTP client untuk interservice communication |

### Library Python (Search Service)

| Library | Versi | Kegunaan |
|---------|-------|----------|
| fastapi | 0.104.0 | Framework REST API |
| uvicorn | 0.24.0 | ASGI server |
| elasticsearch | 7.13.4 | Elasticsearch driver |
| pydantic | 2.5.0 | Data validation |

### Library JavaScript (Frontend)

| Library | Versi | Kegunaan |
|---------|-------|----------|
| vue | 3.4+ | Framework frontend |
| vue-router | 4.2+ | Routing |
| axios | 1.6+ | HTTP client |
| bootstrap | 5.3+ | CSS framework |
| bootstrap-icons | 1.11+ | Icon set |