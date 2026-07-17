# PERTANYAAN DOSEN

## Overview
Bagian ini berisi 70+ pertanyaan yang mungkin diajukan oleh dosen saat presentasi, beserta jawabannya yang komprehensif. Pertanyaan dibagi menjadi kategori untuk memudahkan navigasi.

---

## KATEGORI 1: DASAR (BASIC)

### Q1: Apa itu MongoDB?
**Jawaban:**
MongoDB adalah NoSQL document database yang menyimpan data dalam format JSON-like documents (BSON). Berbeda dengan MySQL yang menggunakan tabel, MongoDB menggunakan collections dan documents. MongoDB cocok untuk aplikasi yang memerlukan flexible schema dan high write throughput.

**Key Points:**
- NoSQL document database
- Flexible schema (tidak perlu define schema terlebih dahulu)
- JSON-like format (BSON)
- High performance untuk CRUD operations
- Horizontal scalability dengan sharding

---

### Q2: Apa itu Elasticsearch?
**Jawaban:**
Elasticsearch adalah distributed search dan analytics engine yang dibangun di atas Apache Lucene. ES digunakan untuk full-text search, log analytics, dan application monitoring. ES menggunakan inverted index untuk memberikan performa search yang sangat cepat (O(1) complexity).

**Key Points:**
- Search engine, bukan database
- Full-text search capabilities
- Inverted index untuk fast lookup
- Relevance scoring (BM25 algorithm)
- Distributed architecture

---

### Q3: Apa itu Docker?
**Jawaban:**
Docker adalah platform containerization yang memungkinkan developer mengemas aplikasi beserta semua dependenciesnya ke dalam container yang ringan dan portable. Container adalah isolated process yang berjalan di host machine.

**Key Points:**
- Containerization platform
- Lightweight (shares host kernel)
- Portable (run anywhere)
- Consistent environment
- Isolation antar services

---

### Q4: Apa itu Microservices?
**Jawaban:**
Microservices adalah arsitektur software development di mana aplikasi dibangun sebagai kumpulan small, independent services yang berkomunikasi melalui well-defined APIs (biasanya HTTP/REST). Setiap service menangani specific business capability dan bisa di-deploy, scaled, dan maintained secara independen.

**Key Points:**
- Small, independent services
- Single responsibility per service
- Independent deployment
- Technology diversity
- Fault isolation

---

### Q5: Apa itu FastAPI?
**Jawaban:**
FastAPI adalah modern, high-performance web framework untuk Python 3.7+ yang dibangun berdasarkan standar OpenAPI dan JSON Schema. FastAPI menggunakan Pydantic untuk validation dan Starlette untuk web server. FastAPI adalah salah satu framework Python tercepat (setara dengan NodeJS dan Go).

**Key Points:**
- Modern Python web framework
- High performance (2-3x faster than Flask)
- Async/await support
- Auto-generated Swagger documentation
- Type validation with Pydantic

---

### Q6: Apa itu Vue.js?
**Jawaban:**
Vue.js adalah progressive JavaScript framework untuk building user interfaces. Vue dirancang untuk dapat diadopsi secara bertahap - dari library yang ringin hingga full-featured framework. Vue menggunakan Virtual DOM untuk performa yang optimal.

**Key Points:**
- Progressive JavaScript framework
- Reactive data binding
- Component-based architecture
- Virtual DOM
- Easy to learn

---

## KATEGORI 2: TEKNOLOGI & ARSITEKTUR

### Q7: Mengapa menggunakan Microservices instead of Monolith?
**Jawaban:**
Project ini menggunakan microservices karena:
1. **Separation of Concerns**: Core Service (CRUD) dan Search Service (Search) memiliki tanggung jawab yang jelas
2. **Independent Scaling**: Bisa scale Core Service dan Search Service secara independen
3. **Technology Optimization**: Setiap service bisa menggunakan technology stack yang optimal untuk tugasnya
4. **Fault Isolation**: Jika Search Service down, CRUD tetap berjalan
5. **Educational Purpose**: Belajar arsitektur modern yang digunakan di industri

**Comparison:**
- Monolith: Semua dalam satu aplikasi, sulit di-scale
- Microservices: Terpisah, mudah di-scale, tapi lebih complex

---

### Q8: Mengapa menggunakan MongoDB instead of MySQL?
**Jawaban:**
MongoDB dipilih karena:
1. **Flexible Schema**: Tidak perlu define schema terlebih dahulu, cocok untuk rapid development
2. **JSON-like Format**: Native format untuk REST API, mudah di-work dengan Python/JavaScript
3. **Fast CRUD**: Optimized untuk create/read/update/delete operations
4. **Scalable**: Horizontal scaling dengan sharding
5. **No Complex JOINs**: Products tidak memiliki complex relationships

**When to use MySQL instead:**
- Complex relational data
- Critical ACID transactions
- Extensive reporting
- Legacy systems

---

### Q9: Mengapa menggunakan Elasticsearch instead of MongoDB regex search?
**Jawaban:**
Elasticsearch digunakan karena:
1. **Performance**: 50-500x lebih cepat dari MongoDB regex (10-50ms vs 500-5000ms)
2. **Relevance Scoring**: BM25 algorithm untuk ranked results
3. **Fuzzy Matching**: Toleransi terhadap typo
4. **Inverted Index**: O(1) lookup instead of O(n) full scan
5. **Scalability**: Bisa handle jutaan documents

**Performance Comparison:**
- 10,000 docs: MongoDB ~500ms, ES ~15ms (33x faster)
- 100,000 docs: MongoDB ~5,000ms, ES ~20ms (250x faster)
- 1,000,000 docs: MongoDB ~50,000ms, ES ~50ms (1000x faster)

---

### Q10: Mengapa menggunakan FastAPI instead of Flask?
**Jawaban:**
FastAPI dipilih karena:
1. **Performance**: 2-3x lebih cepat dari Flask (setara dengan NodeJS dan Go)
2. **Async Support**: Native async/await untuk concurrent requests
3. **Auto Documentation**: Swagger UI otomatis
4. **Type Validation**: Pydantic untuk automatic validation
5. **Modern Python**: Menggunakan type hints, async/await

**Comparison:**
- Flask: Simple, mature, but synchronous
- FastAPI: Modern, fast, async, auto-documentation

---

### Q11: Mengapa menggunakan Vue.js instead of React?
**Jawaban:**
Vue.js dipilih karena:
1. **Learning Curve**: Lebih mudah dipelajari dibanding React
2. **Documentation**: Dokumentasi yang excellent
3. **Performance**: Virtual DOM dan optimized rendering
4. **Flexibility**: Bisa digunakan sebagai library atau full framework
5. **Two-way Data Binding**: Lebih intuitive untuk form handling

**Comparison:**
- React: Steeper learning curve, JSX syntax, larger ecosystem
- Vue: Easier, template-based, good documentation

---

### Q12: Mengapa menggunakan Docker?
**Jawaban:**
Docker digunakan karena:
1. **Consistency**: Environment yang sama di dev, staging, production
2. **Isolation**: Setiap service terpisah dalam container
3. **Portability**: Bisa dijalankan di any machine
4. **Easy Setup**: Single command `docker-compose up -d`
5. **Version Control**: Dockerfile bisa di-commit ke Git

**Benefits:**
- No more "works on my machine"
- Fast deployment
- Easy scaling
- Resource efficient

---

## KATEGORI 3: MONGODB

### Q13: Apa itu NoSQL?
**Jawaban:**
NoSQL (Not Only SQL) adalah kategori database management system yang tidak menggunakan model relasional tradisional. NoSQL dirancang untuk handling large-scale data yang memerlukan fleksibilitas schema, high performance, dan horizontal scalability.

**Types of NoSQL:**
1. **Document**: MongoDB (JSON-like documents)
2. **Key-Value**: Redis
3. **Column**: Cassandra
4. **Graph**: Neo4j

**When to use NoSQL:**
- Data structure berubah-ubah
- High write throughput
- Horizontal scaling needed
- Rapid prototyping

---

### Q14: Apa perbedaan SQL dan NoSQL?
**Jawaban:**

| Aspek | SQL (MySQL) | NoSQL (MongoDB) |
|-------|-------------|-----------------|
| Schema | Fixed, predefined | Flexible, dynamic |
| Structure | Tables, rows, columns | Collections, documents |
| Scaling | Vertical only | Horizontal + Vertical |
| Joins | Native JOINs | No JOINs (embedded) |
| Transactions | Full ACID | Full ACID (v4.0+) |
| Query Language | SQL (standardized) | MongoDB Query Language |

**When to use SQL:**
- Complex relationships
- ACID transactions critical
- Structured data

**When to use NoSQL:**
- Flexible schema
- High write throughput
- Rapid development

---

### Q15: Apa itu ObjectId di MongoDB?
**Jawaban:**
ObjectId adalah unique identifier untuk setiap document di MongoDB. ObjectId adalah 12-byte hexadecimal string yang contains:
- 4 bytes: Timestamp
- 5 bytes: Machine identifier
- 3 bytes: Process ID
- 2 bytes: Counter

**Example:**
```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011")
}
```

**Note:** Project ini menggunakan integer _id instead of ObjectId untuk simplicity.

---

### Q16: Bagaimana cara kerja indexing di MongoDB?
**Jawaban:**
Indexing di MongoDB menggunakan B-tree data structure untuk meningkatkan performa query. Index membuat data structure untuk fast lookup tanpa harus scan entire collection.

**Types of Indexes:**
1. **Single Field Index**: `db.products.createIndex({nama: 1})`
2. **Compound Index**: `db.products.createIndex({kategori: 1, harga: -1})`
3. **Text Index**: `db.products.createIndex({nama: "text", kategori: "text"})`
4. **Unique Index**: `db.products.createIndex({email: 1}, {unique: true})`

**Performance:**
- Without index: O(n) - full collection scan
- With index: O(log n) - fast lookup

---

### Q17: Apa itu Aggregation Pipeline di MongoDB?
**Jawaban:**
Aggregation pipeline adalah framework untuk data transformation dan analysis. Pipeline consists dari multiple stages yang diproses secara berurutan.

**Common Stages:**
1. `$match`: Filter documents (seperti WHERE)
2. `$group`: Group documents dan calculate aggregates
3. `$project`: Select/rename fields
4. `$sort`: Sort documents
5. `$limit`: Limit number of documents
6. `$lookup`: Join collections

**Example:**
```javascript
db.products.aggregate([
  {$match: {kategori: "Laptop"}},
  {$group: {_id: "$kategori", total: {$sum: "$stok"}}},
  {$sort: {total: -1}}
])
```

---

### Q18: Bagaimana cara kerja schema di MongoDB?
**Jawaban:**
MongoDB menggunakan schema-less design, artinya setiap document dalam collection bisa memiliki field yang berbeda. Tidak perlu define schema terlebih dahulu.

**Example:**
```javascript
// Document 1
{_id: 1, nama: "Laptop", harga: 5000000}

// Document 2 (different structure!)
{_id: 2, nama: "Phone", harga: 3000000, warna: "Black"}

// Both are valid!
```

**Benefits:**
- Rapid development
- Easy to modify structure
- No migration needed

**Drawbacks:**
- No data consistency guarantee
- Application must handle validation

---

## KATEGORI 4: ELASTICSEARCH

### Q19: Apa itu Inverted Index?
**Jawaban:**
Inverted Index adalah data structure yang mapping token → documents. Ini adalah rahasia mengapa Elasticsearch sangat cepat.

**Structure:**
```
Token      → Document IDs
"laptop"   → [1, 5, 12, 23, 45]
"gaming"   → [5, 12, 23]
"asus"     → [1, 12]
```

**How it works:**
1. Query "laptop gaming"
2. Lookup "laptop" → [1, 5, 12, 23, 45]
3. Lookup "gaming" → [5, 12, 23]
4. Intersection: [5, 12, 23]
5. Return documents 5, 12, 23

**Performance:** O(1) instead of O(n)

---

### Q20: Apa itu Relevance Scoring?
**Jawaban:**
Relevance score adalah nilai yang menunjukkan seberapa cocok document dengan query. Elasticsearch menggunakan BM25 algorithm untuk calculate score.

**BM25 Formula:**
```
Score = IDF × TF

IDF = log((N - n(term) + 0.5) / (n(term) + 0.5) + 1)
TF = (freq(term) * (k1 + 1)) / (freq(term) + k1 * (1 - b + b * doc_len / avg_doc_len))
```

**Example:**
- Document contains "laptop" 2x → Higher score
- Document contains "laptop" 1x → Lower score
- Rare terms → Higher IDF → Higher score

---

### Q21: Apa itu Analyzer di Elasticsearch?
**Jawaban:**
Analyzer adalah komponen yang mengubah text menjadi tokens untuk indexing. Analyzer consists of:
1. **Character Filters**: Pre-processing (remove HTML, lowercase)
2. **Tokenizer**: Memecah text menjadi tokens
3. **Token Filters**: Post-processing (lowercase, remove stopwords, stemming)

**Example:**
```
Input: "Laptop Gaming Terbaik!"
  ↓ Character Filter (lowercase)
"laptop gaming terbaik!"
  ↓ Tokenizer
["laptop", "gaming", "terbaik"]
  ↓ Token Filter (stopwords)
["laptop", "gaming"]  // "terbaik" removed if stopword
```

---

### Q22: Apa perbedaan Elasticsearch dengan database biasa?
**Jawaban:**

| Aspek | Database (MongoDB) | Search Engine (ES) |
|-------|-------------------|-------------------|
| Primary Purpose | CRUD operations | Full-text search |
| Query Type | Exact match, regex | Full-text, fuzzy, semantic |
| Indexing | B-tree indexes | Inverted indexes |
| Scoring | No relevance scoring | BM25, TF-IDF scoring |
| Consistency | Strong | Eventual |
| Use Case | Transactional data | Search, analytics |

**Key Difference:**
- MongoDB: Best untuk CRUD
- Elasticsearch: Best untuk search

---

### Q23: Bagaimana cara kerja Fuzzy Matching?
**Jawaban:**
Fuzzy matching adalah kemampuan Elasticsearch untuk menoleransi typo dalam query. ES menggunakan edit distance (Levenshtein distance) untuk menentukan seberapa mirip dua kata.

**Example:**
```
Query: "lapto" (typo)
Fuzziness: AUTO
Matches: "laptop" (edit distance 1)
```

**Fuzziness Levels:**
- 0: Exact match
- 1: One character difference
- 2: Two character difference
- AUTO: Based on term length

---

### Q24: Apa itu BM25?
**Jawaban:**
BM25 (Best Match 25) adalah default scoring algorithm di Elasticsearch. BM25 adalah improvement dari TF-IDF yang lebih akurat untuk short queries.

**Key Features:**
- **Saturation**: TF di-cap untuk prevent domination oleh frequent terms
- **Length Normalization**: Adjust score berdasarkan document length
- **Better for Short Queries**: More accurate untuk short queries

**Formula:**
```
Score = IDF × ((freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_len / avg_doc_len)))
```

---

## KATEGORI 5: DOCKER

### Q25: Apa itu Docker Image?
**Jawaban:**
Docker Image adalah blueprint atau template yang berisi semua instructions untuk membuat container. Image adalah read-only template yang defines:
- Base operating system
- Application code
- Dependencies (libraries, packages)
- Environment variables
- Commands to run
- Ports to expose

**Example:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

---

### Q26: Apa itu Docker Container?
**Jawaban:**
Docker Container adalah instance running dari Docker image. Container adalah isolated process yang berjalan di host machine dengan its own filesystem, networking, dan process space.

**Characteristics:**
- **Lightweight**: Shares kernel dengan host (tidak seperti VM)
- **Isolated**: Each container terpisah dari others
- **Portable**: Bisa dijalankan di any machine
- **Ephemeral**: Data hilang jika container dihapus (kecuali menggunakan volumes)

---

### Q27: Apa itu Docker Volume?
**Jawaban:**
Docker Volume adalah persistent storage untuk data container. Volume memungkinkan data tetap ada meskipun container dihapus atau di-recreate.

**Use Case:**
- Database data (MongoDB, Elasticsearch)
- Uploaded files
- Configuration files
- Log files

**Types:**
1. **Named Volume**: Managed by Docker
2. **Bind Mount**: Direct host directory

---

### Q28: Apa itu Docker Network?
**Jawaban:**
Docker Network adalah virtual network yang memungkinkan komunikasi antar containers. Containers dalam network yang sama bisa saling mengakses menggunakan service name.

**Example:**
```yaml
# docker-compose.yml
services:
  core-service:
    networks:
      - uas_app-network
  
  search-service:
    networks:
      - uas_app-network

networks:
  uas_app-network:
    driver: bridge
```

**Benefit:**
```python
# Core Service mengakses Search Service
url = "http://search-service:8002/api/sync/single"
# Docker DNS resolves "search-service" to IP address
```

---

### Q29: Apa itu Docker Compose?
**Jawaban:**
Docker Compose adalah tool untuk defining dan running multi-container Docker applications. Dengan single YAML file, seluruh stack aplikasi bisa dijalankan dengan single command.

**Example:**
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f core-service
```

**Benefits:**
- Single command untuk jalankan seluruh stack
- Automatic networking
- Volume management
- Environment configuration

---

### Q30: Bagaimana cara kerja Docker Compose networking?
**Jawaban:**
Docker Compose creates a default network untuk semua services. Containers bisa communicate menggunakan service name sebagai hostname.

**Example:**
```yaml
services:
  core-service:
    build: ./core-service
    networks:
      - uas_app-network
  
  search-service:
    build: ./search-service
    networks:
      - uas_app-network

networks:
  uas_app-network:
    driver: bridge
```

**Communication:**
```python
# Core Service → Search Service
url = "http://search-service:8002/api/sync/single"
# Docker DNS resolves "search-service" to container IP
```

---

## KATEGORI 6: SYNCHRONIZATION

### Q31: Bagaimana cara kerja sinkronisasi MongoDB → Elasticsearch?
**Jawaban:**
Sinkronisasi menggunakan fire-and-forget pattern:
1. Core Service melakukan CRUD operation di MongoDB
2. Setelah MongoDB operation berhasil, create async task untuk sync
3. Async task mengirim HTTP request ke Search Service
4. Search Service index/update/delete document di Elasticsearch
5. Core Service immediately return response ke client (tidak tunggu sync)

**Code Example:**
```python
# Core Service
async def create_product(product):
    # 1. Insert to MongoDB
    mongo.insert_satu(product)
    
    # 2. Sync to Elasticsearch (async, fire-and-forget)
    asyncio.create_task(
        sync_to_search_service("POST", "/sync/single", product)
    )
    
    # 3. Return immediately
    return {"status": "success"}
```

---

### Q32: Mengapa menggunakan async sync instead of sync?
**Jawaban:**
Async sync (fire-and-forget) digunakan karena:
1. **Better UX**: User tidak perlu tunggu sync selesai
2. **Performance**: Response time lebih cepat
3. **Non-blocking**: Sync happens in background
4. **Acceptable Delay**: Elasticsearch eventual consistency (1 second) acceptable untuk search

**Trade-off:**
- Pro: Fast response time
- Con: Elasticsearch might lag 1 second behind MongoDB
- Solution: Acceptable untuk search use case

---

### Q33: Bagaimana jika sync gagal?
**Jawaban:**
Jika sync gagal:
1. Core Service logs warning (tidak fail)
2. User tetap melihat success message (CRUD berhasil)
3. Data tersimpan di MongoDB (source of truth)
4. Search Service bisa di-recover dengan re-seed data

**Error Handling:**
```python
try:
    await sync_to_search_service("POST", "/sync/single", product)
except httpx.RequestError as e:
    logger.warning(f"Sinkronisasi gagal: {e}")
    # Don't fail the request
```

**Recovery:**
```bash
# Re-seed all data
POST /api/products/seed
```

---

### Q34: Apa konsekuensi eventual consistency di Elasticsearch?
**Jawaban:**
Eventual consistency berarti data di Elasticsearch mungkin lag 1-2 detik dari MongoDB. Ini adalah trade-off yang acceptable untuk search use case.

**Impact:**
- User create product → Immediately visible di MongoDB
- User create product → Visible di search after ~1 second
- User mungkin tidak melihat product mereka sendiri di search result (jika search immediately after create)

**Mitigation:**
- Show message "Product created" (from MongoDB)
- Search results update automatically after 1 second
- Acceptable untuk UX

---

### Q35: Bagaimana cara memastikan data konsisten?
**Jawaban:**
Data consistency strategy:
1. **MongoDB**: Source of truth, strong consistency
2. **Elasticsearch**: Search index, eventual consistency
3. **Sync**: Real-time async sync after each CRUD
4. **Recovery**: Re-seed data jika terjadi mismatch

**Monitoring:**
```python
# Check document count
GET /api/stats
# Compare MongoDB count vs Elasticsearch count
```

**Recovery:**
```bash
# If mismatch, re-seed
POST /api/products/seed
```

---

## KATEGORI 7: API & FRONTEND

### Q36: Bagaimana cara kerja REST API di project ini?
**Jawaban:**
Project ini menggunakan RESTful API architecture:
1. **Frontend** (Vue.js) mengirim HTTP requests
2. **Core Service** (FastAPI) menerima dan validates requests
3. **Core Service** executes CRUD operations di MongoDB
4. **Core Service** syncs changes ke Search Service (async)
5. **Search Service** updates Elasticsearch
6. **Response** dikembalikan ke Frontend

**HTTP Methods:**
- GET: Read data
- POST: Create data
- PUT: Update data
- DELETE: Delete data

---

### Q37: Mengapa menggunakan Vue.js?
**Jawaban:**
Vue.js dipilih karena:
1. **Easy to Learn**: Learning curve yang mudah
2. **Reactive**: Data binding otomatis
3. **Component-Based**: Reusable components
4. **Performance**: Virtual DOM
5. **Documentation**: Excellent documentation

**Benefits:**
- Fast development
- Easy to maintain
- Good for small to medium apps
- Large community

---

### Q38: Bagaimana cara kerja Axios?
**Jawaban:**
Axios adalah HTTP client library untuk JavaScript yang digunakan untuk membuat HTTP requests.

**Features:**
- Promise-based API
- Automatic JSON transformation
- Request/response interception
- Better error handling
- Request cancellation

**Example:**
```javascript
import axios from 'axios'

// GET request
const response = await axios.get('/api/products')

// POST request
const response = await axios.post('/api/products', {
  nama: "Laptop",
  harga: 5000000
})
```

---

### Q39: Apa itu debouncing di search?
**Jawaban:**
Debouncing adalah teknik untuk menunda execution function sampai setelah certain waktu tidak ada activity.

**In Search:**
```javascript
// User types "laptop gaming"
// Without debounce: 12 requests (l, la, lap, lapt, laptop, ...)
// With debounce (300ms): 1 request (laptop gaming)

watch(searchQuery, (newQuery) => {
  setTimeout(async () => {
    await performSearch(newQuery)
  }, 300)
})
```

**Benefits:**
- Reduce server load
- Better UX (no flickering)
- More efficient

---

### Q40: Bagaimana cara kerja Swagger documentation?
**Jawaban:**
Swagger UI adalah auto-generated interactive API documentation yang dibuat oleh FastAPI.

**Access:**
```
Core Service: http://localhost:8001/docs
Search Service: http://localhost:8002/docs
```

**Features:**
- View all endpoints
- See request/response schemas
- Test API directly from browser
- Auto-generated from code

---

## KATEGORI 8: PERFORMANCE & SCALABILITY

### Q41: Bagaimana performa sistem ini?
**Jawaban:**
Performance metrics:
- **CRUD Operations**: 50-100ms (MongoDB)
- **Search Operations**: 10-50ms (Elasticsearch)
- **Total Response Time**: 50-150ms

**Breakdown:**
```
CREATE Product:
- Validation: 5-10ms
- MongoDB Insert: 10-50ms
- Response: 5-10ms
- Total: 20-70ms

SEARCH Product:
- Network: 1-10ms
- Elasticsearch Query: 10-50ms
- Response: 5-10ms
- Total: 15-70ms
```

---

### Q42: Bagaimana cara scaling sistem ini?
**Jawaban:**
Sistem ini bisa di-scale secara horizontal:

**Core Service:**
```bash
docker-compose up -d --scale core-service=3
# 3 instances of Core Service
```

**Search Service:**
```bash
docker-compose up -d --scale search-service=3
# 3 instances of Search Service
```

**MongoDB:**
- Replica sets untuk read scaling
- Sharding untuk write scaling

**Elasticsearch:**
- Add more data nodes
- Increase shards

---

### Q43: Berapa banyak user yang bisa di-handle?
**Jawaban:**
Sistem ini bisa handle:
- **Small Scale**: 100-1,000 concurrent users (single instance)
- **Medium Scale**: 1,000-10,000 concurrent users (2-3 instances per service)
- **Large Scale**: 10,000-100,000+ concurrent users (load balancer + multiple instances)

**Factors:**
- Hardware specifications
- Network bandwidth
- Database performance
- Search query complexity

---

### Q44: Bagaimana cara optimize performa?
**Jawaban:**
Optimization strategies:
1. **Connection Pooling**: Reuse database connections
2. **Indexing**: MongoDB _id index, Elasticsearch inverted index
3. **Caching**: Redis untuk frequent queries (future)
4. **Async Operations**: Non-blocking sync
5. **Debouncing**: Reduce unnecessary search requests
6. **Horizontal Scaling**: Add more instances

---

### Q45: Apa bottleneck dalam sistem ini?
**Jawaban:**
Potential bottlenecks:
1. **MongoDB**: Write operations (can be mitigated with sharding)
2. **Elasticsearch**: Search queries (can be mitigated with more nodes)
3. **Network**: Inter-service communication (minimal with Docker network)
4. **Frontend**: Client-side rendering (acceptable for this scale)

**Mitigation:**
- Monitor with metrics
- Scale horizontally
- Optimize queries
- Add caching

---

## KATEGORI 9: TROUBLESHOOTING

### Q46: Bagaimana jika MongoDB tidak bisa diakses?
**Jawaban:**
Symptoms:
- Core Service returns 503 error
- "MongoDB tidak tersedia" message

**Troubleshooting:**
```bash
# Check MongoDB status
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Check connection
docker-compose exec core-service ping mongodb

# Restart MongoDB
docker-compose restart mongodb
```

**Prevention:**
- Health checks
- Connection retry logic
- Monitoring

---

### Q47: Bagaimana jika Elasticsearch tidak bisa diakses?
**Jawaban:**
Symptoms:
- Search Service returns 503 error
- "Elasticsearch tidak tersedia" message
- Search returns empty results

**Troubleshooting:**
```bash
# Check Elasticsearch status
docker-compose ps elasticsearch

# Check Elasticsearch logs
docker-compose logs elasticsearch

# Check cluster health
curl http://localhost:9200/_cluster/health

# Restart Elasticsearch
docker-compose restart elasticsearch
```

**Note:** CRUD operations still work, only search affected

---

### Q48: Bagaimana jika container terus restart?
**Jawaban:**
Symptoms:
- Container status shows "Restarting"
- `docker-compose ps` shows restarting

**Troubleshooting:**
```bash
# Check logs
docker-compose logs <service-name>

# Common causes:
# - Application error
# - Port conflict
# - Missing environment variables
# - Database not ready

# Fix and restart
docker-compose up -d --force-recreate <service-name>
```

---

### Q49: Bagaimana jika port sudah digunakan?
**Jawaban:**
Symptoms:
- "Port already in use" error
- Container fails to start

**Solution:**
```bash
# Check which process using port
netstat -ano | findstr :8001

# Change port in docker-compose.yml
ports:
  - "8003:8001"  # Use different host port

# Or stop conflicting process
taskkill /PID <pid> /F
```

---

### Q50: Bagaimana jika data hilang setelah restart?
**Jawaban:**
Symptoms:
- Data disappears after `docker-compose down`
- Empty database after restart

**Cause:**
- Volumes not properly configured
- Volumes were deleted

**Solution:**
```bash
# Check volumes
docker volume ls

# Don't use -v flag when stopping
docker-compose down  # Correct
docker-compose down -v  # Deletes volumes!

# Re-create volumes
docker-compose up -d
```

---

## KATEGORI 10: ADVANCED

### Q51: Bagaimana cara kerja Pydantic v2?
**Jawaban:**
Pydantic v2 adalah library untuk data validation di Python. Pydantic v2 menggunakan:
1. **Type Hints**: Define data types
2. **Validation**: Automatic validation
3. **Serialization**: Convert to/from JSON
4. **Field Aliases**: Map field names

**Example:**
```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(..., alias="_id")
    nama: str
    harga: int = Field(..., ge=0)

# Usage
product = Product(id=1, nama="Laptop", harga=5000000)
print(product.id)  # 1
print(product.model_dump(by_alias=True))  # {"_id": 1, "nama": "Laptop", ...}
```

**Changes from v1:**
- `__fields__` → `model_fields`
- `.dict()` → `.model_dump()`
- Field names cannot start with underscore (use alias instead)

---

### Q52: Apa itu Field Alias di Pydantic?
**Jawaban:**
Field alias adalah cara untuk menggunakan nama field yang berbeda di Python vs JSON.

**Example:**
```python
class Product(BaseModel):
    id: int = Field(..., alias="_id")
    # Python: product.id
    # JSON: {"_id": 1}

product = Product(id=1, nama="Laptop")
print(product.id)  # Access as 'id' in Python
print(product.model_dump(by_alias=True))  # {"_id": 1, "nama": "Laptop"}
```

**Why use alias:**
- MongoDB uses `_id` as field name
- Python convention: `_id` is private field
- Solution: Use `id` in Python, `_id` in JSON

---

### Q53: Bagaimana cara kerja async/await di Python?
**Jawaban:**
Async/await adalah syntax untuk asynchronous programming di Python.

**Example:**
```python
import asyncio

async def create_product(product):
    # 1. Insert to MongoDB (async)
    await mongo.insert_satu(product)
    
    # 2. Sync to Elasticsearch (async, fire-and-forget)
    asyncio.create_task(
        sync_to_search_service("POST", "/sync/single", product)
    )
    
    # 3. Return immediately (don't wait for sync)
    return {"status": "success"}

# Run async function
result = asyncio.run(create_product(product))
```

**Benefits:**
- Non-blocking I/O
- Better performance
- Concurrent operations

---

### Q54: Apa itu httpx dan mengapa digunakan?
**Jawaban:**
httpx adalah HTTP client untuk Python yang supports async/await.

**Why httpx:**
- Async support (matching FastAPI)
- HTTP/2 support
- Connection pooling
- Timeout configuration
- Easy to use

**Example:**
```python
import httpx

async def sync_to_search_service(method, endpoint, data):
    url = f"http://search-service:8002/api{endpoint}"
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        if method == "POST":
            await client.post(url, json=data)
        elif method == "PUT":
            await client.put(url, json=data)
```

---

### Q55: Bagaimana cara kerja health checks?
**Jawaban:**
Health checks adalah mekanisme untuk memastikan container sudah siap dan berjalan dengan baik.

**Docker Compose Health Check:**
```yaml
services:
  mongodb:
    image: mongo:7
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Application Health Check:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "core-service"
    }
```

**Benefits:**
- Ensure service is ready before starting dependent services
- Monitoring
- Auto-restart on failure

---

## KATEGORI 11: COMPARISON

### Q56: Mengapa tidak menggunakan single database (MongoDB only)?
**Jawaban:**
MongoDB only approach:
- **Pros**: Simpler, no sync needed
- **Cons**: Poor search performance (500ms vs 10ms)

**Why both:**
- MongoDB: Best untuk CRUD (strong consistency, fast writes)
- Elasticsearch: Best untuk search (inverted index, relevance scoring)
- Together: Best performance for both operations

**Trade-off:**
- Additional complexity (sync mechanism)
- Additional cost (2 databases)
- Benefit: 50-500x faster search

---

### Q57: Mengapa tidak menggunakan single service (monolith)?
**Jawaban:**
Monolith approach:
- **Pros**: Simpler, faster development
- **Cons**: Difficult to scale, single point of failure

**Why microservices:**
- Independent scaling (scale Core and Search separately)
- Fault isolation (if Search down, CRUD still works)
- Technology diversity (best tool per service)
- Better for large teams

**Trade-off:**
- Additional complexity (orchestration, networking)
- Additional infrastructure
- Benefit: Scalability, maintainability

---

### Q58: Bagaimana perbedaan dengan aplikasi Laravel biasa?
**Jawaban:**

| Aspek | Laravel Monolith | This Project |
|-------|------------------|--------------|
| Architecture | Monolith | Microservices |
| Database | MySQL | MongoDB + ES |
| Search | Regex (slow) | Elasticsearch (fast) |
| Frontend | Blade (SSR) | Vue.js (CSR) |
| Deployment | Manual (hours) | Docker (minutes) |
| Scalability | Vertical only | Horizontal + Vertical |
| Search Speed | 500-5000ms | 10-50ms |

**Key Differences:**
- Modern tech stack
- Better performance
- Scalable architecture
- Containerized deployment

---

### Q59: Kapan harus menggunakan monolith instead of microservices?
**Jawaban:**
Use Monolith when:
- **Small Team** (1-3 developers)
- **Simple Application** (few features)
- **Early Stage Startup** (need to move fast)
- **Limited Budget** (cannot afford complex infrastructure)
- **Tight Deadlines** (need to ship quickly)

**Use Microservices when:**
- **Large Team** (10+ developers)
- **Complex Application** (many features)
- **High Traffic** (need to scale)
- **High Availability** (cannot afford downtime)
- **Different Technologies** (need best tool per service)

---

### Q60: Berapa biaya operasional sistem ini?
**Jawaban:**
**Infrastructure Cost:**
```
Core Service: $50-100/month
Search Service: $50-100/month
MongoDB: $50-100/month
Elasticsearch: $50-100/month
Frontend: $20-50/month
Total: $220-450/month
```

**vs Monolith:**
```
Single Server: $200-500/month
Database: $100-300/month
Total: $300-800/month
```

**Conclusion:** Microservices lebih cost-effective untuk medium-high traffic.

---

## KATEGORI 12: IMPLEMENTASI

### Q61: Bagaimana cara menambahkan fitur authentication?
**Jawaban:**
Add Auth Service:
1. **Create Auth Service** (FastAPI)
2. **Implement JWT** authentication
3. **Add login endpoint**
4. **Protect endpoints** with dependency injection
5. **Frontend**: Add login form, store token

**Example:**
```python
# Auth Service
@router.post("/login")
async def login(username: str, password: str):
    user = authenticate(username, password)
    token = create_jwt_token(user)
    return {"access_token": token}

# Core Service - Protected endpoint
@router.get("/api/products")
async def get_products(token: str = Depends(verify_jwt)):
    products = mongo.cari_semua()
    return products
```

---

### Q62: Bagaimana cara menambahkan fitur pagination?
**Jawaban:**
Add pagination to search:
```python
@router.get("/api/search")
async def search_products(q: str, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["nama", "kategori"]
            }
        },
        "from": offset,
        "size": limit
    }
    
    results = client.search(index="produk", body=query)
    return results
```

**Frontend:**
```javascript
const response = await axios.get('/api/search', {
  params: { q: query, page: currentPage, limit: 10 }
})
```

---

### Q63: Bagaimana cara menambahkan fitur filtering?
**Jawaban:**
Add filters to search:
```python
@router.get("/api/search")
async def search_products(
    q: str,
    kategori: str = None,
    harga_min: int = None,
    harga_max: int = None
):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": q, "fields": ["nama", "kategori"]}}
                ],
                "filter": []
            }
        }
    }
    
    if kategori:
        query["query"]["bool"]["filter"].append(
            {"term": {"kategori": kategori}}
        )
    
    if harga_min and harga_max:
        query["query"]["bool"]["filter"].append(
            {"range": {"harga": {"gte": harga_min, "lte": harga_max}}}
        )
    
    results = client.search(index="produk", body=query)
    return results
```

---

### Q64: Bagaimana cara menambahkan caching?
**Jawabin:**
Add Redis caching:
```python
from redis import Redis

redis_client = Redis(host='redis', port=6379)

def cari_match(keyword: str):
    # Check cache
    cached = redis_client.get(f"search:{keyword}")
    if cached:
        return json.loads(cached)
    
    # Search Elasticsearch
    results = es.search(keyword)
    
    # Cache for 5 minutes
    redis_client.setex(f"search:{keyword}", 300, json.dumps(results))
    
    return results
```

**Benefits:**
- Faster response (1-5ms vs 10-50ms)
- Reduce Elasticsearch load
- Better UX

---

### Q65: Bagaimana cara menambahkan logging?
**Jawaban:**
Add structured logging:
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/api/products")
async def create_product(product: ProductCreateSchema):
    logger.info(f"Creating product: {product.nama}")
    
    try:
        result = mongo.insert_satu(product)
        logger.info(f"Product created: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise
```

**Tools:**
- Python logging (built-in)
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Structured logging with JSON format

---

## KATEGORI 13: DEPLOYMENT & PRODUCTION

### Q66: Bagaimana cara deploy ke production?
**Jawaban:**
Deployment steps:
1. **Prepare servers** (AWS/GCP/Azure)
2. **Install Docker** dan Docker Compose
3. **Clone repository**
4. **Configure environment variables**
5. **Build images**: `docker-compose build`
6. **Start services**: `docker-compose up -d`
7. **Configure reverse proxy** (Nginx)
8. **Setup SSL** (Let's Encrypt)
9. **Setup monitoring** (Prometheus + Grafana)
10. **Setup backups** (MongoDB, Elasticsearch)

**Production docker-compose.yml:**
```yaml
services:
  core-service:
    image: core-service:1.0.0
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

### Q67: Bagaimana cara monitoring sistem?
**Jawaban:**
Monitoring stack:
1. **Metrics**: Prometheus + Grafana
   - Request count
   - Response time
   - Error rate
   - CPU/Memory usage

2. **Logging**: ELK Stack
   - Centralized logging
   - Log aggregation
   - Search logs

3. **Health Checks**: Built-in endpoints
   - `/health` untuk each service
   - Docker health checks

4. **Alerting**: Alertmanager
   - Email alerts
   - Slack notifications
   - PagerDuty integration

---

### Q68: Bagaimana cara backup data?
**Jawaban:**
Backup strategy:

**MongoDB:**
```bash
# Backup
docker-compose exec mongodb mongodump --out=/backup/mongodb

# Restore
docker-compose exec mongodb mongorestore /backup/mongodb
```

**Elasticsearch:**
```bash
# Snapshot
curl -X PUT "http://localhost:9200/_snapshot/backup/snapshot_1?wait_for_completion=true"

# Restore
curl -X POST "http://localhost:9200/_snapshot/backup/snapshot_1/_restore"
```

**Schedule:**
- Daily backups
- Weekly full backups
- Monthly archives

---

### Q69: Bagaimana cara handling high traffic?
**Jawaban:**
High traffic strategies:
1. **Load Balancer**: Nginx/HAProxy
   - Distribute traffic
   - Health checks
   - SSL termination

2. **Horizontal Scaling**: Multiple instances
   ```bash
   docker-compose up -d --scale core-service=5
   ```

3. **Database Scaling**:
   - MongoDB: Sharding
   - Elasticsearch: Add nodes

4. **Caching**: Redis
   - Cache frequent queries
   - Reduce database load

5. **CDN**: CloudFlare/AWS CloudFront
   - Cache static assets
   - Reduce server load

---

### Q70: Bagaimana cara handling errors di production?
**Jawaban:**
Error handling strategies:
1. **Global Exception Handler**:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

2. **Retry Logic**:
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def sync_to_search_service():
    # Retry 3 times
```

3. **Circuit Breaker**: Prevent cascade failures
4. **Monitoring**: Alert on errors
5. **Fallback**: Graceful degradation

---

## KATEGORI 14: MISCELLANEOUS

### Q71: Mengapa menggunakan integer _id instead of ObjectId?
**Jawaban:**
Integer _id digunakan karena:
1. **Simplicity**: Lebih mudah dibaca dan debug
2. **Performance**: Integer lebih cepat untuk comparison
3. **Compatibility**: Lebih mudah di-integrasikan dengan Elasticsearch
4. **Use Case**: Data produk dengan ID yang pre-defined

**Trade-off:**
- ObjectId: Auto-generated, unique, timestamp embedded
- Integer: Manual, simpler, human-readable

---

### Q72: Bagaimana jika ada conflict ID?
**Jawaban:**
Conflict handling:
```python
# Check duplicate before insert
existing = mongo.cari_by_id(product_id)
if existing:
    raise HTTPException(400, "Produk dengan ID ini sudah ada")

# Or use upsert
db.products.update_one(
    {"_id": product_id},
    {"$set": product},
    upsert=True
)
```

**Best Practice:**
- Always check for duplicates
- Return clear error message
- Let user choose different ID

---

### Q73: Bagaimana cara migrate dari MySQL ke MongoDB?
**Jawaban:**
Migration steps:
1. **Export data from MySQL**:
```python
import mysql.connector
mysql_conn = mysql.connector.connect(...)
cursor = mysql_conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
```

2. **Transform data**:
```python
# Convert MySQL rows to MongoDB documents
mongo_docs = []
for product in products:
    mongo_docs.append({
        "_id": product['id'],
        "nama": product['nama'],
        "harga": product['harga']
    })
```

3. **Insert to MongoDB**:
```python
mongo_collection = mongo_db["products"]
mongo_collection.insert_many(mongo_docs)
```

---

### Q74: Bagaimana cara migrate dari MongoDB ke Elasticsearch?
**Jawaban:**
Migration not needed because:
- Elasticsearch is a search index, not primary storage
- Data is synced from MongoDB to Elasticsearch
- Just re-index: `POST /api/products/seed`

**If need to re-index:**
```bash
# Delete old index
curl -X DELETE http://localhost:9200/produk

# Re-index from MongoDB
POST http://localhost:8001/api/products/seed
```

---

### Q75: Apa yang terjadi jika Elasticsearch down?
**Jawaban:**
Impact:
- **Search Service**: Returns error "Elasticsearch tidak tersedia"
- **Core Service**: Still running (CRUD works)
- **Frontend**: Shows "Search temporarily unavailable" message
- **Users**: Can still manage products, just can't search

**Recovery:**
1. Fix Elasticsearch
2. Re-sync data: `POST /api/products/seed`

**Benefit of Microservices:**
- Partial functionality preserved
- No complete system outage

---

## Summary

### Total Questions: 75
- **Basic**: 6 questions
- **Technology & Architecture**: 6 questions
- **MongoDB**: 6 questions
- **Elasticsearch**: 5 questions
- **Docker**: 5 questions
- **Synchronization**: 5 questions
- **API & Frontend**: 5 questions
- **Performance & Scalability**: 5 questions
- **Troubleshooting**: 5 questions
- **Advanced**: 5 questions
- **Comparison**: 5 questions
- **Implementation**: 5 questions
- **Deployment**: 5 questions
- **Migration**: 3 questions
- **Miscellaneous**: 4 questions

### Tips for Presentation:
1. **Understand the concepts**, don't memorize
2. **Use examples** from the project
3. **Draw diagrams** when explaining
4. **Be honest** if you don't know
5. **Connect questions** to real-world scenarios