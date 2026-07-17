# RINGKASAN PROJECT

## Nama Project
**Sistem Manajemen Produk dengan Microservices, MongoDB, dan Elasticsearch**

## Tujuan
Membangun sistem manajemen produk yang scalable menggunakan arsitektur microservices dengan database MongoDB untuk penyimpanan dan Elasticsearch untuk pencarian full-text yang optimal.

## Studi Kasus
Permasalahan pencarian data produk yang semakin lambat seiring bertambahnya data ketika menggunakan regex MongoDB. Diperlukan solusi yang lebih efisien untuk pencarian full-text dengan performa tinggi.

## Teknologi
- **Frontend**: Vue.js 3 + Bootstrap 5
- **Backend**: FastAPI (Python 3.12)
- **Database**: MongoDB 7.0
- **Search Engine**: Elasticsearch 8.15.0
- **Containerization**: Docker & Docker Compose

## Arsitektur
```
┌─────────────┐
│   Vue.js    │ (Frontend - Port 3000)
│  Frontend   │
└──────┬──────┘
       │ HTTP/REST API
       ▼
┌─────────────┐
│ Core Service│ (FastAPI - Port 8001)
│  (CRUD)     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MongoDB   │ (Port 27017)
│  (Storage)  │
└─────────────┘

       │ Sync
       ▼
┌─────────────┐
│Search Service│ (FastAPI - Port 8002)
│  (Search)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Elasticsearch│ (Port 9200)
│  (Search)    │
└─────────────┘
```

## Fitur Utama
1. **CRUD Produk**: Create, Read, Update, Delete produk
2. **Full-Text Search**: Pencarian produk menggunakan Elasticsearch
3. **Real-time Sync**: Sinkronisasi otomatis MongoDB → Elasticsearch
4. **Bulk Seed**: Import data massal dari JSON
5. **REST API**: API lengkap dengan dokumentasi Swagger
6. **Responsive UI**: Interface yang mobile-friendly

## Hasil Akhir
- Sistem CRUD yang berjalan optimal dengan MongoDB
- Pencarian full-text yang cepat dan relevan menggunakan Elasticsearch
- Sinkronisasi real-time antara MongoDB dan Elasticsearch
- Arsitektur microservices yang scalable dan maintainable
- Dokumentasi lengkap untuk presentasi akademik

## Tim
- Developed by: [Nama Mahasiswa]
- NIM: [NIM]
- Mata Kuliah: Topik Khusus
- Semester: 6
- Tahun: 2026