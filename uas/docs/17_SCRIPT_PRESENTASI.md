# SCRIPT PRESENTASI

## Overview
Bagian ini berisi script presentasi yang terstruktur untuk presentasi akademik. Script ini mencakup 10 slide utama yang dapat dibaca langsung saat presentasi.

---

## SLIDE 1: PEMBUKA

### Title: Sistem Manajemen Produk dengan Microservices, MongoDB, dan Elasticsearch

**Script:**
```
"Assalamualaikum warrahmatullahi wabarrakatu.

Puji syukur kehadirat Allah SWT yang telah memberikan kita kesempatan untuk 
menyampaikan presentasi project UAS mata kuliah Topik Khusus.

Nama saya [Nama Mahasiswa], NIM [NIM].

Tema project saya adalah 'Sistem Manajemen Produk dengan Microservices, 
MongoDB, dan Elasticsearch'.

Project ini dibangun untuk menyelesaikan permasalahan pencarian data yang 
lambat dalam aplikasi CRUD tradisional.

Mari saya jelaskan secara detail."
```

**Visual:**
- Title slide dengan nama project
- Nama dan NIM
- Logo/icon untuk MongoDB, Elasticsearch, Docker, FastAPI, Vue.js

---

## SLIDE 2: LATAR BELAKANG

### Title: Mengapa Project Ini Dibuat?

**Script:**
```
"Sebelum membahas solusi, mari kita bahas permasalahan yang dihadapi.

Di era digital saat ini, data semakin banyak. Bayangkan:

Tahun 2020: 1,000 produk
Tahun 2024: 100,000 produk
Tahun 2025: 1,000,000+ produk

Masalah muncul ketika kita menggunakan aplikasi CRUD biasa dengan 
MongoDB regex search:

1. Pencarian menjadi lambat - untuk 100,000 produk, search bisa 
   memakan 5 detik!

2. Tidak ada relevance scoring - hasil search tidak diurutkan 
   berdasarkan relevansi

3. Tidak ada fuzzy matching - typo tidak ketemu

4. Monolith architecture - sulit di-scale

Oleh karena itu, diperlukan solusi yang lebih baik."
```

**Visual:**
- Diagram pertumbuhan data
- Screenshot aplikasi dengan search lambat
- Problem statement

---

## SLIDE 3: SOLUSI

### Title: Solusi: Microservices + MongoDB + Elasticsearch

**Script:**
```
"Solusi yang saya usulkan adalah arsitektur microservices dengan 
dua database:

1. MongoDB - untuk CRUD operations
   - Fast write performance
   - Flexible schema
   - Strong consistency

2. Elasticsearch - untuk full-text search
   - 50-500x lebih cepat dari regex
   - Relevance scoring dengan BM25
   - Fuzzy matching

3. Microservices Architecture
   - Core Service: CRUD operations
   - Search Service: Search operations
   - Independent scaling
   - Fault isolation

4. Docker - untuk containerization
   - Consistent environment
   - Easy deployment
   - Single command setup"
```

**Visual:**
- Architecture diagram
- Technology stack
- Performance comparison chart

---

## SLIDE 4: ARSITEKTUR SISTEM

### Title: Arsitektur Microservices

**Script:**
```
"Ini adalah arsitektur sistem yang dibangun:

Frontend (Vue.js) pada port 3000
    ↓ HTTP/REST API
Core Service (FastAPI) pada port 8001
    ↓ CRUD Operations
MongoDB pada port 27017
    ↓ Async Sync
Search Service (FastAPI) pada port 8002
    ↓ Search Operations
Elasticsearch pada port 9200

Semua services berjalan dalam Docker containers yang terhubung 
melalui Docker network.

Keuntungan arsitektur ini:
1. Separation of concerns - setiap service punya tanggung jawab jelas
2. Independent scaling - bisa scale Core dan Search secara terpisah
3. Fault isolation - jika Search down, CRUD tetap jalan
4. Technology diversity - pilih best tool per service"
```

**Visual:**
- Full architecture diagram
- Component responsibilities
- Communication flow

---

## SLIDE 5: MONGODB

### Title: MongoDB - Primary Database

**Script:**
```
"MongoDB adalah NoSQL document database yang digunakan untuk 
penyimpanan utama data produk.

Mengapa MongoDB?
1. Flexible Schema - tidak perlu define schema terlebih dahulu
2. JSON-like format - native untuk REST API
3. Fast CRUD - optimized untuk create/read/update/delete
4. Scalable - horizontal scaling dengan sharding

Struktur data:
Database: uas_db
Collection: products
Document: {
  _id: 1,
  nama: "Laptop Asus ROG",
  kategori: "Laptop",
  harga: 18999000,
  stok: 15,
  spesifikasi: "AMD Ryzen 9, RAM 16GB"
}

Operasi yang digunakan:
- insert_one() - create product
- find() - read all products
- find_one() - read single product
- update_one() - update product
- delete_one() - delete product"
```

**Visual:**
- MongoDB logo
- Document structure example
- CRUD operations diagram

---

## SLIDE 6: ELASTICSEARCH

### Title: Elasticsearch - Search Engine

**Script:**
```
"Elasticsearch adalah search engine yang digunakan untuk 
full-text search. Ini adalah jantung dari fitur search 
pada aplikasi ini.

Konsep penting Elasticsearch:

1. Inverted Index - mapping token → documents
   Contoh: "laptop" → [1, 5, 12, 23, 45]
   Ini yang membuat search menjadi sangat cepat!

2. Relevance Scoring - BM25 algorithm
   Hasil search diurutkan berdasarkan relevansi

3. Analyzer - memecah text menjadi tokens
   "Laptop Gaming" → ["laptop", "gaming"]

4. Fuzzy Matching - toleransi terhadap typo
   "lapto" akan tetap ketemu "laptop"

Performa:
- 10,000 dokumen: ~15ms
- 100,000 dokumen: ~20ms
- 1,000,000 dokumen: ~50ms

Vs MongoDB regex:
- 100,000 dokumen: ~5,000ms

Elasticsearch 250x lebih cepat!"
```

**Visual:**
- Elasticsearch logo
- Inverted index diagram
- Performance comparison chart

---

## SLIDE 7: MICROSERVICES

### Title: Microservices Architecture

**Script:**
"""
Project ini menggunakan arsitektur microservices dengan 2 services:

1. Core Service (FastAPI - Port 8001)
   - CRUD operations
   - MongoDB integration
   - Sync to Search Service
   
2. Search Service (FastAPI - Port 8002)
   - Full-text search
   - Elasticsearch integration
   - Sync endpoints

Mengapa microservices?
1. Independent Scaling - scale Core dan Search terpisah
2. Fault Isolation - jika Search down, CRUD tetap jalan
3. Technology Optimization - best tool per service
4. Team Collaboration - tim bisa kerja parallel

Komunikasi antar service:
- REST API (HTTP)
- JSON format
- Async fire-and-forget pattern

Setelah CRUD operation di MongoDB, Core Service langsung 
mengirim data ke Search Service secara async, tanpa menunggu.
"""
**Visual:**
- Microservices diagram
- Service responsibilities
- Communication flow

---

## SLIDE 8: DOCKER

### Title: Docker - Containerization

**Script:**
"""
Semua services dijalankan menggunakan Docker containers.

Docker Compose configuration:
- 5 containers total
- Automatic networking
- Volume management untuk data persistence
- Health checks untuk semua services

Commands:
docker-compose up -d    # Start all services
docker-compose down     # Stop all services
docker-compose logs     # View logs

Keuntungan Docker:
1. Consistency - environment yang sama di dev dan production
2. Portability - bisa dijalankan di any machine
3. Isolation - setiap service terpisah
4. Easy Setup - single command untuk jalankan seluruh stack

Volumes:
- mongodb_data - untuk MongoDB data
- elasticsearch_data - untuk Elasticsearch data

Network:
- uas_app-network - bridge network untuk komunikasi antar containers
"""
**Visual:**
- Docker logo
- Container architecture
- docker-compose.yml snippet

---

## SLIDE 9: DEMO CRUD & SEARCH

### Title: Demo - CRUD dan Search

**Script:**
"""
Sekarang saya akan demonstrate aplikasi ini:

1. CRUD Operations:
   - Create product baru
   - Read all products
   - Update product
   - Delete product
   
2. Search Operations:
   - Search dengan keyword "laptop"
   - Show relevance scoring
   - Fuzzy matching dengan typo

3. Synchronization:
   - Show real-time sync MongoDB → Elasticsearch
   - Verify data consistency

Mari kita mulai:
[Live demo dengan browser]

Seperti yang bisa dilihat:
- CRUD operations sangat cepat (50-100ms)
- Search sangat cepat (10-50ms)
- Data tersinkronisasi secara real-time
"""
**Visual:**
- Live demo di browser
- Show Swagger UI
- Show search results

---

## SLIDE 10: KESIMPULAN

### Title: Kesimpulan dan Terima Kasih

**Script:**
"""
Kesimpulan:

Project ini berhasil membangun sistem manajemen produk dengan:
1. Microservices architecture - scalable dan maintainable
2. MongoDB - fast CRUD operations
3. Elasticsearch - 50-500x faster search
4. Docker - consistent deployment
5. Real-time sync - data konsisten antar database

Hasil yang dicapai:
- CRUD operations: 50-100ms
- Search operations: 10-50ms
- 250x faster than MongoDB regex
- Scalable architecture
- Production-ready

Pelajaran yang dipelajari:
1. Modern architecture patterns
2. Database selection (SQL vs NoSQL vs Search Engine)
3. Containerization dengan Docker
4. Real-time data synchronization
5. Performance optimization

Terima kasih atas perhatiannya.

Saya siap untuk menjawab pertanyaan dari dosen.

Assalamualaikum warrahmatullahi wabarrakatu.
"""
**Visual:**
- Summary points
- Key achievements
- Q&A prompt

---

## PRESENTASI TIPS

### 1. Timing
```
Total presentation time: 15-20 minutes
- Slide 1 (Pembuka): 1 minute
- Slide 2 (Latar Belakang): 2 minutes
- Slide 3 (Solusi): 2 minutes
- Slide 4 (Arsitektur): 2 minutes
- Slide 5 (MongoDB): 2 minutes
- Slide 6 (Elasticsearch): 2 minutes
- Slide 7 (Microservices): 2 minutes
- Slide 8 (Docker): 1 minute
- Slide 9 (Demo): 3-5 minutes
- Slide 10 (Kesimpulan): 1 minute
- Q&A: 5-10 minutes
```

### 2. Speaking Tips
1. **Speak clearly** dan dengan confidence
2. **Make eye contact** dengan dosen
3. **Use gestures** untuk explain diagrams
4. **Pause** after important points
5. **Be enthusiastic** tentang project

### 3. Demo Tips
1. **Test beforehand** - pastikan semua services running
2. **Have backup** - screenshot jika demo gagal
3. **Explain as you go** - don't just click
4. **Show the code** - occasionally show backend code
5. **Highlight key features** - search, sync, performance

### 4. Handling Questions
1. **Listen carefully** to the question
2. **Repeat/paraphrase** if needed
3. **Be honest** if you don't know
4. **Use examples** from the project
5. **Draw diagrams** if helpful

### 5. Common Questions to Prepare
- "Why microservices instead of monolith?"
- "Why MongoDB instead of MySQL?"
- "Why Elasticsearch instead of MongoDB search?"
- "How does sync work?"
- "What if Elasticsearch is down?"
- "How to scale this system?"
- "What is the performance?"

---

## BACKUP PLAN

### If Demo Fails:
1. **Have screenshots ready** of working application
2. **Show Swagger UI** instead of frontend
3. **Explain the code** without running
4. **Use Postman** untuk test API

### If Questions Are Difficult:
1. **Be honest**: "Saya belum terlalu dalam memahami itu, tapi..."
2. **Relate to project**: "Dalam project ini, saya..."
3. **Ask for clarification**: "Bisa dijelaskan lebih detail?"
4. **Take note**: "Saya akan research lebih lanjut tentang itu"

---

## MATERIALS CHECKLIST

### Before Presentation:
- [ ] Laptop charged
- [ ] Docker running
- [ ] All services running (`docker-compose ps`)
- [ ] Browser ready with:
  - Frontend (localhost:3000)
  - Swagger UI (localhost:8001/docs)
  - Swagger UI (localhost:8002/docs)
- [ ] Presentation slides ready
- [ ] Script printed/available
- [ ] Backup screenshots
- [ ] Internet connection (if needed)

### During Presentation:
- [ ] Speak clearly
- [ ] Make eye contact
- [ ] Explain diagrams
- [ ] Demo the application
- [ ] Answer questions confidently

---

## CONCLUSION

Presentation ini mencakup:
1. **10 slides** dengan script lengkap
2. **Demo guide** untuk live demonstration
3. **Tips for presentation** untuk sukses
4. **Backup plan** jika ada masalah
5. **Q&A preparation** dengan common questions

Good luck dengan presentasi!