# BAB 3: KEBUTUHAN FUNGSIONAL

## 3.1 Daftar Kebutuhan Fungsional

| Kode | Nama Fungsi | Deskripsi | Prioritas |
|------|-------------|-----------|-----------|
| F-01 | Melihat Daftar Produk | Sistem menampilkan seluruh data produk dalam bentuk tabel | Tinggi |
| F-02 | Melihat Detail Produk | Sistem menampilkan detail satu produk berdasarkan ID | Tinggi |
| F-03 | Menambah Produk | Sistem menambahkan data produk baru ke database | Tinggi |
| F-04 | Mengubah Produk | Sistem mengubah data produk yang sudah ada | Tinggi |
| F-05 | Menghapus Produk | Sistem menghapus data produk dari database | Tinggi |
| F-06 | Seed Data | Sistem mengisi database dengan dataset dari file products.json | Tinggi |
| F-07 | Pencarian Full-Text | Sistem mencari produk menggunakan Elasticsearch | Tinggi |
| F-08 | Sinkronisasi Data | Core Service mengirim data ke Search Service saat CRUD | Sedang |
| F-09 | Melihat Status Sistem | Sistem menampilkan status koneksi database dan service | Rendah |
| F-10 | Melihat Statistik Index | Sistem menampilkan statistik index Elasticsearch | Rendah |

## 3.2 Spesifikasi Kebutuhan Fungsional

### F-01: Melihat Daftar Produk

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna dapat melihat seluruh data produk yang tersimpan di MongoDB |
| **Endpoint** | `GET /api/products` (Core Service) |
| **Method** | GET |
| **Request** | Tidak ada |
| **Response Sukses** | `{ "status": "success", "data": [...], "total": 12 }` |
| **Response Gagal** | `{ "status": "error", "message": "MongoDB tidak tersedia" }` |
| **Skenario** | 1. Pengguna membuka halaman Products<br>2. Frontend memanggil GET /api/products<br>3. Core Service mengambil data dari MongoDB<br>4. Data ditampilkan dalam tabel |

### F-02: Melihat Detail Produk

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna dapat melihat detail satu produk berdasarkan ID |
| **Endpoint** | `GET /api/products/{id}` (Core Service) |
| **Method** | GET |
| **Parameter** | `id` (integer) - ID produk |
| **Response Sukses** | `{ "status": "success", "data": { ... } }` |
| **Response Gagal** | `{ "status": "error", "message": "Produk dengan ID {id} tidak ditemukan" }` |

### F-03: Menambah Produk

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna menambahkan data produk baru |
| **Endpoint** | `POST /api/products` (Core Service) |
| **Method** | POST |
| **Request Body** | `{ "_id": int, "nama": string, "kategori": string, "harga": int, "stok": int, "spesifikasi": string }` |
| **Response Sukses** | Status 201, `{ "status": "success", "message": "Produk ID {id} berhasil dibuat" }` |
| **Response Gagal** | Status 400 jika ID sudah ada, Status 503 jika MongoDB tidak tersedia |
| **Skenario** | 1. Pengguna mengisi form tambah produk<br>2. Frontend memanggil POST /api/products<br>3. Core Service insert ke MongoDB<br>4. Core Service sinkronisasi ke Search Service via POST /api/sync<br>5. Response dikirim ke frontend |

### F-04: Mengubah Produk

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna mengubah data produk yang sudah ada |
| **Endpoint** | `PUT /api/products/{id}` (Core Service) |
| **Method** | PUT |
| **Parameter** | `id` (integer) - ID produk yang akan diubah |
| **Request Body** | `{ "nama"?: string, "kategori"?: string, "harga"?: int, "stok"?: int, "spesifikasi"?: string }` |
| **Response Sukses** | `{ "status": "success", "message": "Produk ID {id} berhasil diupdate" }` |
| **Response Gagal** | Status 404 jika produk tidak ditemukan |

### F-05: Menghapus Produk

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna menghapus data produk |
| **Endpoint** | `DELETE /api/products/{id}` (Core Service) |
| **Method** | DELETE |
| **Parameter** | `id` (integer) - ID produk yang akan dihapus |
| **Response Sukses** | `{ "status": "success", "message": "Produk ID {id} berhasil dihapus" }` |
| **Response Gagal** | Status 404 jika produk tidak ditemukan |

### F-06: Seed Data

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Mengisi database dengan dataset dari file products.json |
| **Endpoint** | `POST /api/products/seed` (Core Service) |
| **Method** | POST |
| **Request** | Tidak ada |
| **Response Sukses** | Status 201, `{ "status": "success", "message": "Berhasil seed {n} produk", "total": 12 }` |
| **Skenario** | 1. Pengguna klik tombol Seed Data<br>2. Frontend memanggil POST /api/products/seed<br>3. Core Service membaca products.json<br>4. Core Service insert ke MongoDB<br>5. Core Service sinkronisasi ke Search Service via POST /api/sync |

### F-07: Pencarian Full-Text

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Pengguna mencari produk menggunakan full-text search Elasticsearch |
| **Endpoint** | `GET /api/search?q={keyword}` (Search Service) |
| **Method** | GET |
| **Parameter** | `q` (string) - Kata kunci pencarian |
| **Response Sukses** | `{ "status": "success", "data": [...], "total": n, "keyword": "..." }` |
| **Response Gagal** | Status 503 jika Elasticsearch tidak tersedia |
| **Skenario** | 1. Pengguna mengetik kata kunci<br>2. Frontend memanggil GET /api/search?q=keyword<br>3. Search Service melakukan multi_match query ke Elasticsearch<br>4. Hasil ditampilkan dalam bentuk card |

### F-08: Sinkronisasi Data

| Aspek | Detail |
|-------|--------|
| **Aktor** | Core Service |
| **Deskripsi** | Core Service mengirim data ke Search Service saat terjadi operasi CRUD |
| **Endpoint** | `POST /api/sync`, `PUT /api/sync/{id}`, `DELETE /api/sync/{id}` (Search Service) |
| **Method** | POST, PUT, DELETE |
| **Trigger** | Operasi create, update, delete pada Core Service |
| **Catatan** | Jika Search Service offline, sinkronisasi dilewati (tidak blocking) |

### F-09: Melihat Status Sistem

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna |
| **Deskripsi** | Halaman Home menampilkan status koneksi MongoDB, Elasticsearch, dan Search Service |
| **Sumber Data** | Core Service (GET /api/products) dan Search Service (GET /api/stats) |
| **Tampilan** | Card dengan icon hijau (terkoneksi) / merah (terputus) |

### F-10: Melihat Statistik Index

| Aspek | Detail |
|-------|--------|
| **Aktor** | Pengguna (via API) |
| **Deskripsi** | Menampilkan statistik index Elasticsearch |
| **Endpoint** | `GET /api/stats` (Search Service) |
| **Method** | GET |
| **Response** | `{ "status": "success", "data": { "document_count": n, "size_in_bytes": n, "status": "connected" } }` |