# LATAR BELAKANG

## Konteks Modern
Di era digital saat ini, data adalah aset paling berharga. Setiap hari, jutaan data baru dihasilkan dari berbagai sumber seperti e-commerce, media sosial, IoT, dan sistem informasi. Kemampuan untuk menyimpan, mengelola, dan mencari data dengan efisien menjadi kunci kesuksesan sistem informasi modern.

## Permasalahan yang Muncul

### 1. **Pertumbuhan Data yang Eksponensial**
```
Tahun 2020: 1,000 produk
    ↓
Tahun 2024: 100,000 produk
    ↓
Tahun 2025: 1,000,000+ produk
```

### 2. **Masalah Pencarian Tradisional**
- **Regex MongoDB**: Cocok untuk data kecil, tetapi sangat lambat untuk dataset besar
- **Full Table Scan**: Setiap pencarian harus scan seluruh collection
- **Tidak ada relevansi**: Hasil pencarian tidak diurutkan berdasarkan relevansi
- **Tidak ada scoring**: Tidak ada perhitungan seberapa cocok hasil dengan query

### 3. **Keterbatasan Monolith Architecture**
- Semua fungsi (CRUD, Search, Authentication) dalam satu aplikasi
- Sulit di-scale secara independen
- Single point of failure
- Maintenance yang kompleks

### 4. **Kebutuhan Bisnis Modern**
- **Real-time search**: User mengharapkan hasil instan
- **Fuzzy matching**: Toleransi terhadap typo
- **Multi-field search**: Pencarian di beberapa field sekaligus
- **Ranking**: Hasil diurutkan berdasarkan relevansi
- **Scalability**: Sistem harus bisa handle pertumbuhan data

## Solusi yang Diusulkan

### Arsitektur Microservices
Memecah sistem menjadi layanan-layanan kecil yang independen:
- **Core Service**: Menangani operasi CRUD
- **Search Service**: Menangani pencarian full-text
- **Frontend**: User interface

### Database Hybrid
- **MongoDB**: Untuk operasi CRUD dan penyimpanan utama
- **Elasticsearch**: Untuk pencarian full-text yang cepat

### Containerization
- **Docker**: Memastikan konsistensi environment
- **Docker Compose**: Orchestration multi-container

## Mengapa Project Ini Penting?

### Akademik
- Menerapkan konsep modern: Microservices, NoSQL, Search Engine
- Integrasi teknologi yang sedang trending di industri
- Best practices dalam arsitektur sistem

### Praktis
- Solusi nyata untuk masalah yang umum di industri
- Performa yang signifikan lebih baik dari solusi tradisional
- Scalable untuk pertumbuhan masa depan

### Inovasi
- Menggabungkan MongoDB (NoSQL) dengan Elasticsearch (Search Engine)
- Real-time synchronization antar database
- Modern tech stack dengan FastAPI dan Vue.js

## Dampak yang Diharapkan
1. **Performa**: Pencarian 10x-100x lebih cepat dari regex MongoDB
2. **Scalability**: Sistem bisa di-scale secara independen
3. **Maintainability**: Codebase yang terorganisir dengan baik
4. **User Experience**: Search experience yang lebih baik
5. **Knowledge**: Pemahaman mendalam tentang modern system architecture