# DEMO APPLICATION

## Overview
Bagian ini berisi panduan lengkap untuk menjalankan dan mendemonstrasikan aplikasi. Panduan ini mencakup setup, testing, dan live demo untuk presentasi.

---

## DAFTAR ISI
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Testing the API](#testing-the-api)
5. [Live Demo Guide](#live-demo-guide)
6. [Troubleshooting](#troubleshooting)

---

## 1. PREREQUISITES

### Software yang Dibutuhkan

#### 1.1 Docker Desktop
- **Download**: https://www.docker.com/products/docker-desktop/
- **Version**: Latest stable
- **Requirements**:
  - Windows 10/11 Pro, Enterprise, atau Education
  - WSL 2 enabled
  - Minimum 4GB RAM
  - Minimum 20GB disk space

**Verifikasi Installation:**
```bash
docker --version
# Output: Docker version 24.0.7, build xxxxx

docker-compose --version
# Output: Docker Compose version v2.23.0
```

#### 1.2 Git (Optional)
- **Download**: https://git-scm.com/downloads
- **Purpose**: Clone repository

**Verifikasi:**
```bash
git --version
# Output: git version 2.43.0.windows.1
```

#### 1.3 Browser
- Chrome, Firefox, atau Edge
- Untuk mengakses Frontend dan Swagger UI

#### 1.4 API Client (Optional)
- Postman: https://www.postman.com/downloads/
- Thunder Client (VS Code extension)
- curl (already installed)

---

## 2. INSTALLATION

### 2.1 Clone Repository

```bash
# Clone repository
git clone https://github.com/fathiyyah28/topik_khusus.git

# Navigate to project directory
cd topik_khusus

# Verify structure
ls -la
# Should see: docker-compose.yml, app/, core-service/, search-service/, frontend/
```

### 2.2 Verify docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  core-service:
    build: ./core-service
    ports:
      - "8001:8001"
    environment:
      - MONGO_URI=mongodb://mongodb:27017
      - SEARCH_SERVICE_URL=http://search-service:8002
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - uas_app-network

  search-service:
    build: ./search-service
    ports:
      - "8002:8002"
    environment:
      - ELASTIC_URI=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - uas_app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - core-service
      - search-service
    networks:
      - uas_app-network

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=uas_db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - uas_app-network

  elasticsearch:
    image: elasticsearch:8.15.0
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - uas_app-network

networks:
  uas_app-network:
    driver: bridge

volumes:
  mongodb_data:
  elasticsearch_data:
```

### 2.3 Verify Project Structure

```
topik_khusus/
├── docker-compose.yml
├── app.py (legacy, ignore)
├── requirements.txt
├── data/
│   └── products.json
├── core-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── routes.py
│       ├── schemas.py
│       ├── mongo_service.py
│       └── config.py
├── search-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── routes.py
│       ├── elastic_service.py
│       └── schemas.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.vue
        ├── main.js
        └── components/
```

---

## 3. RUNNING THE APPLICATION

### 3.1 Start All Services

```bash
# Start all services in detached mode
docker-compose up -d

# Expected output:
# Creating network "topik_khusus_uas_app-network" ...
# Creating volume "topik_khusus_mongodb_data" ...
# Creating volume "topik_khusus_elasticsearch_data" ...
# Building core-service ...
# Building search-service ...
# Building frontend ...
# Creating mongodb ... done
# Creating elasticsearch ... done
# Creating core-service ... done
# Creating search-service ... done
# Creating frontend ... done
```

### 3.2 Verify Services are Running

```bash
# Check all services status
docker-compose ps

# Expected output:
# NAME                    SERVICE              STATUS
# topik_khusus-core-1     core-service         running
# topik_khusus-elastic-1  elasticsearch        running (healthy)
# topik_khusus-front-1    frontend             running
# topik_khusus-mongo-1    mongodb              running (healthy)
# topik_khusus-search-1   search-service       running
```

### 3.3 Check Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs core-service
docker-compose logs search-service
docker-compose logs mongodb
docker-compose logs elasticsearch
docker-compose logs frontend

# Follow logs (real-time)
docker-compose logs -f core-service
```

### 3.4 Verify Health

```bash
# Check Core Service health
curl http://localhost:8001/health
# Expected: {"status":"healthy","service":"core-service"}

# Check Search Service health
curl http://localhost:8002/health
# Expected: {"status":"healthy","service":"search-service"}

# Check MongoDB connection
docker-compose exec core-service python -c "from app import mongo_service as mongo; print(mongo.cek_koneksi())"
# Expected: True

# Check Elasticsearch connection
curl http://localhost:9200/_cluster/health
# Expected: {"cluster_name":"docker-cluster","status":"green",...}
```

### 3.5 Access Application

```
Frontend:      http://localhost:3000
Core Service:  http://localhost:8001
Search Service: http://localhost:8002
Swagger UI:    http://localhost:8001/docs
Swagger UI:    http://localhost:8002/docs
MongoDB:       mongodb://localhost:27017
Elasticsearch: http://localhost:9200
```

---

## 4. TESTING THE API

### 4.1 Seed Data

```bash
# Seed MongoDB with sample data
curl -X POST http://localhost:8001/api/products/seed

# Expected Response:
# {
#   "status": "success",
#   "message": "Berhasil seed 12 produk ke MongoDB dan Elasticsearch",
#   "data": [...],
#   "total": 12
# }
```

### 4.2 Test CRUD Operations

#### CREATE Product
```bash
curl -X POST http://localhost:8001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "_id": 99,
    "nama": "Test Product",
    "kategori": "Test",
    "harga": 100000,
    "stok": 10,
    "spesifikasi": "Test specifications"
  }'

# Expected: 201 Created
# {
#   "status": "success",
#   "message": "Produk ID 99 berhasil dibuat",
#   "data": {...}
# }
```

#### READ All Products
```bash
curl http://localhost:8001/api/products

# Expected: 200 OK
# {
#   "status": "success",
#   "message": "Ditemukan 12 produk",
#   "data": [...],
#   "total": 12
# }
```

#### READ Single Product
```bash
curl http://localhost:8001/api/products/1

# Expected: 200 OK
# {
#   "status": "success",
#   "message": "Produk ditemukan",
#   "data": {...}
# }
```

#### UPDATE Product
```bash
curl -X PUT http://localhost:8001/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Updated Product Name",
    "harga": 20000000
  }'

# Expected: 200 OK
# {
#   "status": "success",
#   "message": "Produk ID 1 berhasil diupdate",
#   "data": {...}
# }
```

#### DELETE Product
```bash
curl -X DELETE http://localhost:8001/api/products/99

# Expected: 200 OK
# {
#   "status": "success",
#   "message": "Produk ID 99 berhasil dihapus",
#   "data": null
# }
```

### 4.3 Test Search Operations

#### Search Products
```bash
curl "http://localhost:8002/api/search?q=laptop"

# Expected: 200 OK
# {
#   "status": "success",
#   "message": "Ditemukan 3 hasil untuk 'laptop'",
#   "data": [...],
#   "total": 3,
#   "keyword": "laptop"
# }
```

#### Search with Fuzzy Matching
```bash
curl "http://localhost:8002/api/search?q=lapto"

# Expected: Results include "laptop" (typo tolerated)
```

#### Get Stats
```bash
curl http://localhost:8002/api/stats

# Expected: 200 OK
# {
#   "status": "success",
#   "data": {
#     "status": "connected",
#     "index": "produk",
#     "document_count": 12,
#     "size_in_bytes": 8162
#   }
# }
```

### 4.4 Test with Postman

#### Import Collection
Create a new Postman collection with these requests:

**Collection Name:** Product Management API

**Requests:**

1. **GET All Products**
   - URL: `http://localhost:8001/api/products`
   - Method: GET

2. **GET Product by ID**
   - URL: `http://localhost:8001/api/products/1`
   - Method: GET

3. **CREATE Product**
   - URL: `http://localhost:8001/api/products`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "_id": 100,
     "nama": "New Product",
     "kategori": "Test",
     "harga": 500000,
     "stok": 20,
     "spesifikasi": "Test specs"
   }
   ```

4. **UPDATE Product**
   - URL: `http://localhost:8001/api/products/1`
   - Method: PUT
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "nama": "Updated Name",
     "harga": 15000000
   }
   ```

5. **DELETE Product**
   - URL: `http://localhost:8001/api/products/100`
   - Method: DELETE

6. **SEARCH Products**
   - URL: `http://localhost:8002/api/search?q=laptop`
   - Method: GET

7. **SEED Data**
   - URL: `http://localhost:8001/api/products/seed`
   - Method: POST

---

## 5. LIVE DEMO GUIDE

### 5.1 Demo Flow (10-15 minutes)

#### Part 1: Introduction (2 minutes)
```
1. Show architecture diagram
2. Explain the problem (slow search)
3. Explain the solution (MongoDB + Elasticsearch)
```

#### Part 2: CRUD Operations (3 minutes)

**Step 1: Show Product List**
```
1. Open browser to http://localhost:3000
2. Show product list (12 products)
3. Explain: "Ini adalah data dari MongoDB"
4. Show response time: ~50ms
```

**Step 2: Create Product**
```
1. Click "Tambah Produk" button
2. Fill form:
   - ID: 13
   - Nama: "MacBook Pro M3"
   - Kategori: "Laptop"
   - Harga: 35000000
   - Stok: 5
   - Spesifikasi: "Apple M3, RAM 18GB, SSD 512GB"
3. Click "Simpan"
4. Show success message
5. Explain: "Product created in MongoDB, syncing to Elasticsearch..."
```

**Step 3: Read Product**
```
1. Click on product card
2. Show product detail
3. Explain: "Data fetched from MongoDB"
```

**Step 4: Update Product**
```
1. Click "Edit" button
2. Change harga to 36000000
3. Click "Update"
4. Show success message
5. Explain: "Updated in MongoDB, syncing to Elasticsearch..."
```

**Step 5: Delete Product**
```
1. Click "Hapus" button
2. Confirm deletion
3. Show success message
4. Explain: "Deleted from MongoDB, syncing to Elasticsearch..."
```

#### Part 3: Search Operations (3 minutes)

**Step 1: Basic Search**
```
1. Go to Search page
2. Type "laptop" in search box
3. Wait for results
4. Show results with relevance scores
5. Explain: "Search menggunakan Elasticsearch, 250x faster than MongoDB regex"
6. Show response time: ~15ms
```

**Step 2: Multi-field Search**
```
1. Clear search
2. Type "gaming"
3. Show results from multiple fields (nama, kategori, spesifikasi)
4. Explain: "Multi-match query across multiple fields"
```

**Step 3: Fuzzy Matching**
```
1. Clear search
2. Type "lapto" (typo)
3. Show results still include "laptop"
4. Explain: "Fuzzy matching tolerates typos"
```

**Step 4: Show Relevance Scoring**
```
1. Search "laptop gaming"
2. Show results ordered by relevance
3. Explain: "BM25 algorithm ranks results by relevance"
4. Show scores if visible
```

#### Part 4: Synchronization (2 minutes)

**Step 1: Show Real-time Sync**
```
1. Create new product via API
2. Immediately search for it
3. Show it appears in search results
4. Explain: "Async sync happens in background"
```

**Step 2: Verify Data Consistency**
```
1. Show MongoDB data (via Compass or CLI)
2. Show Elasticsearch data (via Kibana or API)
3. Explain: "Data is synchronized in real-time"
```

**Step 3: Show Stats**
```
1. Open http://localhost:8002/api/stats
2. Show document count
3. Explain: "Elasticsearch has same data as MongoDB"
```

#### Part 5: Swagger UI Demo (2 minutes)

**Step 1: Show Swagger UI**
```
1. Open http://localhost:8001/docs
2. Show available endpoints
3. Try one endpoint (e.g., GET /api/products)
4. Show auto-generated documentation
5. Explain: "FastAPI auto-generates Swagger documentation"
```

**Step 2: Show Search Service Swagger**
```
1. Open http://localhost:8002/docs
2. Show search endpoint
3. Try search endpoint
4. Show response
```

#### Part 6: Performance Comparison (2 minutes)

**Step 1: Show Performance Metrics**
```
1. Show response times:
   - CRUD: 50-100ms
   - Search: 10-50ms
2. Compare with MongoDB regex:
   - Search: 500-5000ms
3. Explain: "250x faster search with Elasticsearch"
```

**Step 2: Show Architecture Benefits**
```
1. Independent scaling
2. Fault isolation
3. Technology optimization
4. Easy deployment with Docker
```

---

### 5.2 Demo Script

#### Opening
```
"Assalamualaikum warrahmatullahi wabarrakatu.

Saya akan demonstrate aplikasi Sistem Manajemen Produk dengan 
Microservices, MongoDB, dan Elasticsearch.

Mari kita mulai dengan CRUD operations."
```

#### During CRUD Demo
```
"Saya akan membuat product baru dengan ID 13, MacBook Pro M3.

Setelah saya klik Simpan, yang terjadi adalah:
1. Product disimpan di MongoDB (source of truth)
2. Core Service mengirim data ke Search Service secara async
3. Search Service meng-index data di Elasticsearch
4. User langsung dapat response (tidak perlu tunggu sync)

Perhatikan response time-nya sangat cepat, sekitar 50-100ms."
```

#### During Search Demo
```
"Sekarang saya akan search produk dengan keyword 'laptop'.

Yang terjadi:
1. Query dikirim ke Search Service
2. Search Service query Elasticsearch
3. Elasticsearch menggunakan inverted index untuk lookup
4. BM25 algorithm calculate relevance scores
5. Results returned dalam 10-50ms

Ini 250x lebih cepat dari MongoDB regex search yang membutuhkan 
5 detik untuk 100,000 dokumen."
```

#### During Sync Demo
```
"Mari saya tunjukkan sinkronisasi data.

Saya akan create product baru, lalu immediately search.
Anda akan melihat product baru muncul di search results.

Ini adalah eventual consistency - data di Elasticsearch mungkin 
lag 1 detik dari MongoDB, tapi ini acceptable untuk search use case."
```

#### Closing
```
"Seperti yang bisa dilihat:
- CRUD operations sangat cepat (50-100ms)
- Search sangat cepat (10-50ms)
- Data tersinkronisasi secara real-time
- Architecture yang scalable dan maintainable

Terima kasih atas perhatiannya.

Saya siap untuk menjawab pertanyaan."
```

---

## 6. TROUBLESHOOTING

### 6.1 Common Issues

#### Issue 1: Services won't start
```bash
# Check logs
docker-compose logs

# Common causes:
# - Port already in use
# - Docker not running
# - Insufficient resources

# Solution:
# 1. Stop conflicting services
# 2. Restart Docker Desktop
# 3. Increase Docker resources (4GB RAM minimum)
```

#### Issue 2: MongoDB connection error
```bash
# Check MongoDB status
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Verify connection
docker-compose exec core-service ping mongodb
```

#### Issue 3: Elasticsearch connection error
```bash
# Check Elasticsearch status
docker-compose ps elasticsearch

# Check Elasticsearch logs
docker-compose logs elasticsearch

# Restart Elasticsearch
docker-compose restart elasticsearch

# Verify connection
curl http://localhost:9200/_cluster/health
```

#### Issue 4: Frontend not loading
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Check if port 3000 is available
netstat -ano | findstr :3000
```

#### Issue 5: Data not syncing
```bash
# Check Core Service logs
docker-compose logs core-service | grep -i sync

# Check Search Service logs
docker-compose logs search-service | grep -i sync

# Re-seed data
curl -X POST http://localhost:8001/api/products/seed

# Verify Elasticsearch index
curl http://localhost:9200/produk/_search?pretty
```

### 6.2 Reset Everything

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Rebuild all images
docker-compose build --no-cache

# Start fresh
docker-compose up -d

# Seed data
curl -X POST http://localhost:8001/api/products/seed
```

### 6.3 Performance Issues

```bash
# Check resource usage
docker stats

# If high CPU/Memory:
# - Increase Docker resources
# - Scale services horizontally
# - Optimize queries

# Scale Core Service
docker-compose up -d --scale core-service=3

# Scale Search Service
docker-compose up -d --scale search-service=3
```

---

## 7. QUICK REFERENCE

### 7.1 Essential Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart core-service

# View logs
docker-compose logs -f core-service

# Rebuild service
docker-compose build core-service
docker-compose up -d core-service

# Seed data
curl -X POST http://localhost:8001/api/products/seed

# Check status
docker-compose ps

# Access MongoDB shell
docker-compose exec mongodb mongosh

# Access Elasticsearch
curl http://localhost:9200/_cluster/health
```

### 7.2 URLs

```
Frontend:           http://localhost:3000
Core Service:       http://localhost:8001
Search Service:     http://localhost:8002
Swagger (Core):     http://localhost:8001/docs
Swagger (Search):   http://localhost:8002/docs
MongoDB:            mongodb://localhost:27017
Elasticsearch:      http://localhost:9200
```

### 7.3 Test Data

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

### 7.4 Sample Searches

```
"laptop" - Should return laptops
"gaming" - Should return gaming products
"phone" - Should return phones
"lapto" - Should still return laptops (fuzzy matching)
"laptop gaming" - Should return gaming laptops
```

---

## 8. DEMO CHECKLIST

### Before Demo:
- [ ] Docker Desktop is running
- [ ] All services are running (`docker-compose ps`)
- [ ] Frontend is accessible (http://localhost:3000)
- [ ] Swagger UI is accessible (http://localhost:8001/docs)
- [ ] Data is seeded (12 products)
- [ ] Browser is ready with all tabs open
- [ ] Backup screenshots are available
- [ ] Script is printed/available

### During Demo:
- [ ] Speak clearly and confidently
- [ ] Explain each step
- [ ] Show response times
- [ ] Highlight key features
- [ ] Answer questions clearly

### After Demo:
- [ ] Thank the audience
- [ ] Be ready for Q&A
- [ ] Have code examples ready
- [ ] Be prepared to explain architecture decisions

---

## 9. WHAT TO HIGHLIGHT

### Key Features to Show:
1. **Fast CRUD**: 50-100ms response time
2. **Fast Search**: 10-50ms response time
3. **Real-time Sync**: Data syncs automatically
4. **Fuzzy Matching**: Typo tolerance
5. **Relevance Scoring**: Results ordered by relevance
6. **Microservices**: Independent services
7. **Docker**: Easy deployment
8. **Auto Documentation**: Swagger UI

### Key Metrics to Mention:
- 250x faster search than MongoDB regex
- 50-100ms CRUD operations
- 10-50ms search operations
- 12 products in database
- 5 Docker containers
- 13 API endpoints

### Key Architecture Points:
- MongoDB for CRUD (strong consistency)
- Elasticsearch for search (eventual consistency)
- Async sync (fire-and-forget)
- Fault isolation
- Independent scaling

---

## SUMMARY

Demo application ini mencakup:
1. **Installation guide** untuk setup
2. **Testing guide** untuk API testing
3. **Live demo guide** untuk presentasi
4. **Troubleshooting** untuk common issues
5. **Quick reference** untuk commands dan URLs

Follow this guide untuk successful demo!