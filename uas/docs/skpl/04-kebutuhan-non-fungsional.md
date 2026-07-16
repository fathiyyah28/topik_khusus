# BAB 4: KEBUTUHAN NON-FUNGSIONAL

## 4.1 Kebutuhan Kinerja (Performance)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-01 | Waktu Respons API | Seluruh endpoint REST API harus memberikan respons dalam waktu < 2 detik untuk dataset standar (12 produk) |
| NF-02 | Waktu Pencarian | Pencarian full-text di Elasticsearch harus selesai dalam waktu < 1 detik |
| NF-03 | Waktu Muat Halaman | Halaman frontend harus selesai dimuat dalam waktu < 3 detik |
| NF-04 | Throughput | Sistem harus mampu menangani minimal 10 request per detik |

## 4.2 Kebutuhan Keamanan (Security)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-05 | CORS | Sistem mengizinkan akses dari origin mana pun untuk memudahkan development |
| NF-06 | Validasi Input | Semua input dari pengguna divalidasi menggunakan Pydantic sebelum diproses |
| NF-07 | Error Handling | Sistem tidak boleh menampilkan stack trace ke pengguna; error internal dikembalikan sebagai JSON |

## 4.3 Kebutuhan Keandalan (Reliability)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-08 | Ketersediaan | Sistem harus berjalan 24/7 selama masa demonstrasi |
| NF-09 | Toleransi Kesalahan | Jika Search Service tidak tersedia, Core Service tetap dapat berfungsi (sinkronisasi gagal tidak memblokir operasi CRUD) |
| NF-10 | Data Persistence | Data MongoDB dan Elasticsearch disimpan dalam volume Docker agar tidak hilang saat container di-restart |

## 4.4 Kebutuhan Kegunaan (Usability)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-11 | Antarmuka Responsif | Frontend harus responsif dan dapat digunakan di perangkat desktop, tablet, dan mobile |
| NF-12 | Bahasa | Seluruh antarmuka menggunakan Bahasa Indonesia |
| NF-13 | Dokumentasi API | Setiap service memiliki dokumentasi Swagger UI yang dapat diakses di `/docs` |
| NF-14 | Panduan Pengguna | README.md berisi panduan instalasi dan penggunaan yang lengkap |

## 4.5 Kebutuhan Portabilitas (Portability)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-15 | Containerization | Seluruh komponen aplikasi harus dapat dijalankan menggunakan Docker Compose |
| NF-16 | Platform Independence | Aplikasi harus dapat berjalan di sistem operasi Windows, macOS, dan Linux |
| NF-17 | Konfigurasi Lingkungan | Semua konfigurasi dikelola melalui environment variable |

## 4.6 Kebutuhan Kompatibilitas (Compatibility)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-18 | Browser Support | Frontend harus kompatibel dengan Google Chrome, Mozilla Firefox, dan Microsoft Edge versi terbaru |
| NF-19 | RESTful Standard | API mengikuti standar REST dengan response JSON dan HTTP status codes yang sesuai |

## 4.7 Kebutuhan Maintainability (Perawatan)

| Kode | Kebutuhan | Deskripsi |
|------|-----------|-----------|
| NF-20 | Struktur Kode | Source code terdiri dari modul-modul terpisah dengan tanggung jawab yang jelas |
| NF-21 | Dokumentasi Kode | Seluruh fungsi memiliki docstring yang menjelaskan parameter dan return value |
| NF-22 | Logging | Sistem mencatat aktivitas penting ke dalam log dengan level INFO dan ERROR |

## 4.8 Matriks Kelayakan

| Parameter | Target | Metode Pengukuran |
|-----------|--------|-------------------|
| Waktu Respons API | < 2 detik | Pengukuran dengan browser dev tools atau curl |
| Waktu Pencarian ES | < 1 detik | Pengukuran dengan browser dev tools |
| Waktu Muat Halaman | < 3 detik | Pengukuran dengan browser dev tools |
| Ketersediaan | 99% (hanya untuk demo) | Uptime monitoring manual |
| Kompatibilitas Browser | Chrome, Firefox, Edge | Pengujian manual |