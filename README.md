# topik_khusus# 📚 Topik Khusus

> Repository ini berisi seluruh tugas praktikum dan proyek akhir (UAS) pada mata kuliah **Topik Khusus** Program Studi **D4 Teknologi Rekayasa Perangkat Lunak**, **Politeknik Negeri Padang**.

Selama perkuliahan, berbagai teknologi modern dipelajari mulai dari dokumentasi menggunakan Markdown, implementasi database NoSQL, sistem pencarian menggunakan Elasticsearch, caching menggunakan Redis, hingga pembangunan aplikasi berbasis **Microservices** menggunakan **FastAPI**, **Vue.js**, dan **Docker**.

---

# 📂 Struktur Repository

```
topik_khusus
│
├── 📁 Markdown
├── 📁 MongoDB + Elastic
├── 📁 Redis
├── 📁 uas
│
├── .gitignore
└── README.md
```

---

# 📖 Daftar Tugas

## 📝 1. Markdown

Folder ini berisi latihan dan implementasi penggunaan **Markdown (.md)** sebagai bahasa markup sederhana untuk membuat dokumentasi proyek.

### Materi yang dipelajari

- Dasar Markdown
- Heading
- Text Formatting
- Ordered & Unordered List
- Table
- Hyperlink
- Image
- Blockquote
- Code Block
- Checklist
- README Documentation

### Tujuan

Memahami cara membuat dokumentasi proyek yang rapi, mudah dibaca, serta sesuai standar dokumentasi GitHub.

📂 Folder

```
Markdown/
```

---

## 🍃 2. MongoDB + Elasticsearch

Tugas ini membahas implementasi database **MongoDB** beserta integrasinya dengan **Elasticsearch** sebagai mesin pencarian.

### Materi yang dipelajari

- Instalasi MongoDB
- Pembuatan Database
- Collection
- CRUD MongoDB
- Import Dataset
- Instalasi Elasticsearch
- Indexing Data
- Full Text Search
- Query Search
- Analisis Hasil Pencarian

### Tujuan

Memahami penggunaan database NoSQL serta bagaimana Elasticsearch dapat meningkatkan proses pencarian data secara cepat dan efisien.

📂 Folder

```
MongoDB + Elastic/
```

---

## ⚡ 3. Redis

Folder ini berisi implementasi penggunaan **Redis** sebagai database in-memory dan media caching.

### Materi yang dipelajari

- Instalasi Redis
- Konfigurasi Redis
- Key-Value Database
- String
- Hash
- List
- Set
- CRUD Redis
- Cache Data
- Pengujian Redis

### Tujuan

Mempelajari konsep penyimpanan data sementara (cache) menggunakan Redis untuk meningkatkan performa aplikasi.

📂 Folder

```
Redis/
```

---

# 🚀 UAS — Implementasi Microservices

Folder **UAS** merupakan proyek akhir mata kuliah Topik Khusus yang mengimplementasikan arsitektur **Microservices** menggunakan berbagai teknologi modern.

## Teknologi

- FastAPI
- Vue.js
- Docker
- Docker Compose
- MongoDB
- Elasticsearch
- Redis
- REST API

---

## Fitur yang Diimplementasikan

### Backend

- REST API menggunakan FastAPI
- Microservices Architecture
- Integrasi MongoDB
- Integrasi Elasticsearch
- Integrasi Redis
- API Documentation (Swagger)

### Frontend

- Vue.js
- Dashboard
- CRUD Data
- Integrasi API

### DevOps

- Docker
- Docker Compose
- Multi Container
- Network Service
- Volume Management

---

## Arsitektur Sistem

```
                Vue Frontend
                      │
                      │ REST API
                      ▼
              FastAPI Microservice
         ┌──────────┼───────────┐
         │          │           │
         ▼          ▼           ▼
     MongoDB   Elasticsearch   Redis
```

---

# 🛠️ Tech Stack

| Teknologi | Kegunaan |
|-----------|----------|
| Python | Backend Programming |
| FastAPI | REST API Framework |
| Vue.js | Frontend Framework |
| Docker | Containerization |
| Docker Compose | Multi Container |
| MongoDB | NoSQL Database |
| Elasticsearch | Search Engine |
| Redis | Cache Database |
| Markdown | Documentation |
| Git | Version Control |
| GitHub | Repository Management |

---

# 🎯 Capaian Pembelajaran

Melalui seluruh tugas pada repository ini, mahasiswa mempelajari:

- Penulisan dokumentasi proyek menggunakan Markdown.
- Penggunaan database NoSQL MongoDB.
- Implementasi Elasticsearch sebagai search engine.
- Penggunaan Redis sebagai media caching.
- Pembangunan REST API menggunakan FastAPI.
- Pengembangan frontend menggunakan Vue.js.
- Containerization menggunakan Docker.
- Penerapan arsitektur Microservices.
- Integrasi berbagai service dalam satu aplikasi.

---

# 🚀 Cara Menjalankan Project UAS

Masuk ke folder UAS

```bash
cd uas
```

Jalankan Docker Compose

```bash
docker compose up --build
```

Akses aplikasi

Frontend

```
http://localhost:5173
```

Backend API

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# 📂 Repository Summary

| Folder | Deskripsi |
|---------|-----------|
| Markdown | Latihan dokumentasi menggunakan Markdown |
| MongoDB + Elastic | Implementasi MongoDB dan Elasticsearch |
| Redis | Implementasi Redis sebagai cache database |
| uas | Proyek akhir berbasis Microservices |

---

# 👨‍💻 Author

**Fathiyyah Ermita Sari**

D4 Teknologi Rekayasa Perangkat Lunak

Jurusan Teknologi Informasi

Politeknik Negeri Padang

---

⭐ Repository ini dibuat sebagai dokumentasi seluruh tugas dan proyek akhir mata kuliah **Topik Khusus**.