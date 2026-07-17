# TEKNOLOGI YANG DIGUNAKAN

## Overview
Bagian ini menjelaskan secara detail setiap teknologi yang digunakan dalam project ini, mengapa dipilih, kelebihan, kekurangan, dan perbandingan dengan alternatif lain.

---

## 1. VUE.JS 3

### Apa itu Vue.js?
Vue.js adalah progressive JavaScript framework untuk building user interfaces. Vue dirancang untuk dapat diadopsi secara bertahap - dari library yang ringin hingga full-featured framework.

### Mengapa Dipilih?
1. **Learning Curve yang Mudah**: Syntax yang intuitif dan dokumentasi yang excellent
2. **Reactivity System**: Data binding otomatis yang powerful
3. **Component-Based**: Arsitektur komponen yang reusable
4. **Performance**: Virtual DOM dan optimized rendering
5. **Ecosystem**: Vue Router, Vuex/Pinia, Vite untuk tooling

### Fungsinya
- **Frontend Framework**: Membangun user interface yang interaktif
- **Component System**: Komponen reusable untuk form, table, cards
- **State Management**: Mengelola state aplikasi (products, search results)
- **Routing**: Navigasi antar halaman (jika diperlukan)

### Kelebihan
✅ Documentation yang sangat baik  
✅ Learning curve mudah untuk pemula  
✅ Performance tinggi dengan Virtual DOM  
✅ Flexible (bisa digunakan sebagai library atau full framework)  
✅ Two-way data binding  
✅ Single File Components (SFC)  
✅ Komunitas yang besar dan aktif  

### Kekurangan
❌ Ecosystem lebih kecil dibanding React  
❌ Less job opportunities dibanding React  
❌ Some inconsistencies in design patterns  
❌ Too flexible bisa jadi disorienting untuk tim besar  

### Mengapa Bukan React?
| Aspek | Vue.js | React |
|-------|--------|-------|
| Learning Curve | Mudah | Steeper |
| Syntax | Template-based | JSX |
| State Management | Built-in (Pinia) | External (Redux, Context) |
| Performance | Sangat baik | Baik |
| Documentation | Excellent | Baik |
| Popularity | Sedang naik | Sangat tinggi |
| Use Case | Small to Medium apps | Large scale apps |

**Alasan memilih Vue**: Project ini membutuhkan framework yang cepat dipelajari, documentation yang jelas, dan cukup powerful untuk aplikasi medium-scale. Vue memenuhi kebutuhan tersebut dengan baik.

---

## 2. FASTAPI

### Apa itu FastAPI?
FastAPI adalah modern, fast (high-performance) web framework untuk Python 3.7+ yang dibangun berdasarkan standar OpenAPI dan JSON Schema. FastAPI menggunakan Pydantic untuk validation dan Starlette untuk web server.

### Mengapa Dipilih?
1. **Performance**: Salah satu framework Python tercepat (setara dengan NodeJS dan Go)
2. **Async Support**: Native async/await support untuk concurrent requests
3. **Auto Documentation**: Swagger UI dan ReDoc otomatis
4. **Type Hints**: Validasi otomatis menggunakan Pydantic
5. **Modern Python**: Menggunakan fitur Python 3.7+ (type hints, async/await)

### Fungsinya
- **Backend API Server**: Menangani HTTP requests dari frontend
- **CRUD Operations**: Create, Read, Update, Delete products
- **Data Validation**: Validasi request menggunakan Pydantic schemas
- **API Documentation**: Auto-generated Swagger documentation
- **Async Processing**: Concurrent handling untuk sync operations

### Kelebihan
✅ Performance sangat tinggi (2-3x lebih cepat dari Flask)  
✅ Auto-generated API documentation (Swagger)  
✅ Type validation dengan Pydantic  
✅ Native async/await support  
✅ Modern Python features  
✅ Easy to learn dan maintain  
✅ Built-in data validation  
✅ JSON Schema compliant  

### Kekurangan
❌ Relatively new (first release 2018)  
❌ Smaller ecosystem dibanding Flask/Django  
❌ Less tutorials dan community resources  
❌ Some advanced features perlu konfigurasi manual  

### Mengapa Bukan Flask?
| Aspek | FastAPI | Flask |
|-------|---------|-------|
| Performance | Sangat tinggi (async) | Sedang (sync) |
| Auto Documentation | Ya (Swagger) | Tidak (perlu tambahan) |
| Type Validation | Ya (Pydantic) | Tidak (perlu tambahan) |
| Async Support | Native | Perlu setup |
| Learning Curve | Mudah | Sangat mudah |
| Maturity | Baru (2018) | Lama (2010) |
| Use Case | Modern API | Simple API, Microservices |

**Alasan memilih FastAPI**: Project membutuhkan performa tinggi untuk handle concurrent requests (CRUD + sync), auto-generated documentation untuk kemudahan testing, dan modern Python features. FastAPI adalah pilihan terbaik untuk API modern.

---

## 3. DOCKER & DOCKER COMPOSE

### Apa itu Docker?
Docker adalah platform containerization yang memungkinkan developer untuk mengemas aplikasi beserta semua dependenciesnya ke dalam container yang ringan dan portable.

### Docker Compose
Docker Compose adalah tool untuk defining dan running multi-container Docker applications. Dengan single command, seluruh stack aplikasi bisa dijalankan.

### Komponen Docker

#### Image
- Blueprint atau template untuk container
- Contains: code, runtime, libraries, environment variables
- Read-only template
- Built from Dockerfile

#### Container
- Instance running dari image
- Isolated process yang berjalan di host machine
- Has its own filesystem, networking, process space
- Lightweight (shares kernel dengan host)

#### Volume
- Persistent storage untuk data container
- Data tetap ada meskipun container dihapus
- Berguna untuk database (MongoDB, Elasticsearch)
- Bisa di-share antar containers

#### Network
- Virtual network untuk komunikasi antar containers
- Isolated dari host network
- Container bisa saling mengakses menggunakan service name
- Types: Bridge, Host, Overlay

#### Dockerfile
- Text file yang contains instructions untuk build image
- Defines: base image, dependencies, commands, ports
- Example:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

#### Docker Compose
- YAML file untuk define multi-container application
- Defines: services, networks, volumes
- Commands: `up`, `down`, `build`, `restart`

### Mengapa Digunakan?
1. **Consistency**: Environment yang sama di dev, staging, production
2. **Isolation**: Setiap service terpisah dalam container sendiri
3. **Portability**: Bisa dijalankan di any machine dengan Docker
4. **Easy Setup**: Single command untuk jalankan seluruh stack
5. **Version Control**: Dockerfile bisa di-commit ke Git

### Kelebihan
✅ Consistent environment across all machines  
✅ Easy deployment dan scaling  
✅ Resource efficient (lebih ringan dari VM)  
✅ Isolation antar services  
✅ Fast startup time  
✅ Easy rollback (gunakan image sebelumnya)  
✅ Great for microservices architecture  

### Kekurangan
❌ Learning curve untuk pemula  
❌ Additional layer of complexity  
❌ Storage management bisa tricky  
❌ Networking configuration bisa confusing  
❌ Performance overhead (minimal)  

### Perintah Penting
```bash
docker-compose up -d          # Start semua services
docker-compose down           # Stop dan remove semua containers
docker-compose build          # Build images
docker-compose restart <svc>  # Restart specific service
docker-compose logs -f <svc>  # Lihat logs
docker ps                     # List running containers
docker exec -it <container> bash  # Masuk ke container
```

---

## 4. MONGODB

### Apa itu MongoDB?
MongoDB adalah NoSQL document database yang menyimpan data dalam format JSON-like documents (BSON). MongoDB adalah database paling populer untuk modern applications.

### Konsep Dasar

#### Database
- Container untuk collections
- Setiap database memiliki isolated data
- Example: `uas_db`

#### Collection
- Group of documents (setara dengan table di SQL)
- Schema-less (setiap document bisa memiliki field berbeda)
- Example: `products`

#### Document
- Unit dasar data (setara dengan row di SQL)
- Format: JSON-like (BSON)
- Unique identifier: `_id` (ObjectId)
- Example:
```json
{
  "_id": ObjectId("..."),
  "nama": "Laptop Asus",
  "harga": 18999000,
  "stok": 15
}
```

#### ObjectId
- Unique identifier untuk setiap document
- 12-byte hexadecimal string
- Contains: timestamp, machine identifier, process ID, counter
- Auto-generated jika tidak disediakan

### CRUD Operations
```javascript
// CREATE
db.products.insertOne({nama: "Laptop", harga: 5000000})

// READ
db.products.find()                    // All products
db.products.findOne({_id: 1})         // By ID
db.products.find({kategori: "Laptop"}) // By field

// UPDATE
db.products.updateOne(
  {_id: 1},
  {$set: {harga: 6000000}}
)

// DELETE
db.products.deleteOne({_id: 1})
```

### Aggregation Pipeline
Powerful framework untuk data transformation:
```javascript
db.products.aggregate([
  {$match: {kategori: "Laptop"}},
  {$group: {_id: "$kategori", total: {$sum: "$stok"}}},
  {$sort: {total: -1}}
])
```

### Regex Search
```javascript
db.products.find({
  $or: [
    {nama: {$regex: "laptop", $options: "i"}},
    {kategori: {$regex: "laptop", $options: "i"}}
  ]
})
```

### Kelebihan
✅ Schema flexibility (document bisa memiliki structure berbeda)  
✅ Horizontal scalability (sharding)  
✅ High performance untuk write operations  
✅ Rich query language  
✅ Built-in replication dan high availability  
✅ Aggregation framework yang powerful  
✅ JSON-like format (native untuk web apps)  
✅ Great for rapid prototyping  

### Kekurangan
❌ Tidak support JOIN (perlu embedding atau manual join)  
❌ Memory usage tinggi untuk large datasets  
❌ Tidak ada transaction ACID complete (sebelum v4.0)  
❌ Lebih banyak storage space dibanding SQL  
❌ Tidak cocok untuk complex relational data  
❌ Consistency model eventual (bisa ada delay)  

### Mengapa MongoDB untuk Project Ini?
1. **Flexible Schema**: Produk bisa memiliki field berbeda tanpa migration
2. **JSON-like**: Native format untuk REST API
3. **Scalable**: Bisa handle pertumbuhan data
4. **Easy to Use**: Query language yang intuitive
5. **Perfect untuk CRUD**: Operasi create/read/update/delete sangat cepat

---

## 5. ELASTICSEARCH

### Apa itu Elasticsearch?
Elasticsearch adalah distributed search dan analytics engine yang dibangun di atas Apache Lucene. ES digunakan untuk full-text search, log analytics, dan application monitoring.

### Konsep Dasar

#### Index
- Container untuk documents (setara dengan database di SQL)
- Setiap index memiliki mapping (schema definition)
- Example: `produk`

#### Document
- Unit dasar data di Elasticsearch
- Format: JSON
- Unique identifier: `_id`
- Example:
```json
{
  "_id": 1,
  "nama": "Laptop Asus",
  "kategori": "Laptop",
  "harga": 18999000
}
```

#### Analyzer
Proses mengubah text menjadi tokens untuk indexing:
1. **Character Filters**: Pre-processing (remove HTML, lowercase)
2. **Tokenizer**: Memecah text menjadi tokens
3. **Token Filters**: Post-processing (lowercase, remove stopwords, stemming)

Example: "Laptop Gaming Terbaik" → ["laptop", "gaming", "terbaik"]

#### Token
Unit kecil dari text setelah proses analysis. Setiap token di-index di Inverted Index.

#### Inverted Index
Data structure yang mapping token → documents:
```
Token      → Document IDs
"laptop"   → [1, 5, 12, 23, 45]
"gaming"   → [5, 12, 23]
"asus"     → [1, 12]
```

Ini yang membuat search menjadi sangat cepat - langsung lookup token instead of scanning semua documents.

#### Relevance Score
Nilai yang menunjukkan seberapa cocok document dengan query. Di-hitung menggunakan:
- **TF-IDF**: Term Frequency - Inverse Document Frequency
- **BM25**: Better version of TF-IDF (default di ES)
- **Cosine Similarity**: Vector space model

Semakin tinggi score, semakin relevan document.

#### Mapping
Schema definition untuk index:
```json
{
  "mappings": {
    "properties": {
      "nama": {"type": "text", "analyzer": "standard"},
      "harga": {"type": "integer"},
      "stok": {"type": "integer"}
    }
  }
}
```

#### Cluster, Node, Shard, Replica
- **Cluster**: Group of nodes yang bekerja sama
- **Node**: Single instance dari Elasticsearch
- **Shard**: Partition dari index (untuk horizontal scaling)
- **Replica**: Copy dari shard (untuk high availability)

### Bagaimana Proses Search?

```
User Query: "laptop gaming"
    ↓
1. Query Analysis
   "laptop gaming" → ["laptop", "gaming"]
    ↓
2. Lookup Inverted Index
   "laptop" → [1, 5, 12, 23, 45]
   "gaming" → [5, 12, 23]
    ↓
3. Merge Results
   Intersection: [5, 12, 23]
    ↓
4. Calculate Scores
   Doc 5: score 2.45
   Doc 12: score 1.89
   Doc 23: score 1.23
    ↓
5. Sort by Score
   [Doc 5, Doc 12, Doc 23]
    ↓
6. Return Results
```

### Kelebihan
✅ Full-text search yang sangat cepat  
✅ Relevance scoring yang akurat  
✅ Fuzzy matching (toleransi typo)  
✅ Multi-field search  
✅ Faceted search (filtering)  
✅ Horizontal scalability  
✅ Real-time search  
✅ Rich query DSL  
✅ Analytics capabilities  

### Kekurangan
❌ Complex untuk di-setup dan maintain  
❌ Memory intensive  
❌ Steep learning curve  
❌ Overkill untuk small datasets  
❌ Eventually consistent (bukan instant)  
❌ Operational complexity (sharding, replication)  

### Mengapa Elasticsearch untuk Project Ini?
1. **Full-Text Search**: Fitur yang dibutuhkan untuk search produk
2. **Performance**: 10-100x lebih cepat dari regex MongoDB
3. **Relevance**: Hasil diurutkan berdasarkan relevansi
4. **Scalability**: Bisa handle jutaan documents
5. **Fuzzy Matching**: Toleransi terhadap typo user

---

## 6. MICROSERVICES

### Apa itu Microservices?
Microservices adalah arsitektur software development di mana aplikasi dibangun sebagai kumpulan small, independent services yang berkomunikasi melalui well-defined APIs.

### Monolith vs Microservices

#### Monolith Architecture
```
┌─────────────────────────────────┐
│     Single Application          │
│  ┌───────────────────────────┐  │
│  │  CRUD Module              │  │
│  ├───────────────────────────┤  │
│  │  Search Module            │  │
│  ├───────────────────────────┤  │
│  │  Auth Module              │  │
│  ├───────────────────────────┤  │
│  │  Business Logic           │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

#### Microservices Architecture
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Core Svc │  │Search Svc│  │ Auth Svc │
│ (CRUD)   │  │(Search)  │  │ (Login)  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
  ┌──────────────────────────────────┐
  │      Load Balancer / API Gateway │
  └──────────────────────────────────┘
```

### Perbandingan

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Development** | Simple, single codebase | Complex, multiple services |
| **Deployment** | Deploy entire app | Deploy individual services |
| **Scalability** | Scale entire app | Scale specific services |
| **Technology** | Single tech stack | Polyglot (different tech per service) |
| **Fault Isolation** | Single point of failure | Better fault isolation |
| **Team Organization** | Centralized | Distributed teams |
| **Complexity** | Low operational complexity | High operational complexity |
| **Performance** | Faster (no network overhead) | Slower (network calls) |

### Kelebihan Microservices
✅ Independent scaling (scale service yang butuh)  
✅ Independent deployment  
✅ Technology diversity (pilih tech terbaik per service)  
✅ Better fault isolation  
✅ Easier untuk tim besar ( Conway's Law)  
✅ Better maintainability untuk large apps  
✅ Faster development cycles  

### Kekurangan Microservices
❌ Operational complexity (orchestration, monitoring)  
❌ Network latency antar services  
❌ Distributed system challenges (consistency, transactions)  
❌ Harder debugging dan testing  
❌ More infrastructure needed  
❌ Data consistency challenges  

### Mengapa Project Menggunakan Microservices?

#### 1. **Separation of Concerns**
- **Core Service**: Fokus pada CRUD operations
- **Search Service**: Fokus pada search operations
- Setiap service memiliki tanggung jawab yang jelas

#### 2. **Independent Scaling**
- Core Service: Bisa di-scale jika banyak write operations
- Search Service: Bisa di-scale jika banyak search queries
- Tidak perlu scale service yang tidak butuh

#### 3. **Technology Optimization**
- Core Service: Python/FastAPI (optimal untuk CRUD)
- Search Service: Python/FastAPI + Elasticsearch client
- Frontend: Vue.js (optimal untuk UI)

#### 4. **Fault Isolation**
- Jika Search Service down, CRUD tetap berjalan
- Jika Core Service down, search tetap bisa menampilkan data lama
- Tidak ada single point of failure

#### 5. **Team Collaboration**
- Developer A bisa bekerja di Core Service
- Developer B bisa bekerja di Search Service
- Tidak ada conflict antar development

### Komunikasi Antar Service

#### REST API
```python
# Core Service → Search Service
import httpx

async def sinkronisasi_ke_search_service(method: str, endpoint: str, data: dict):
    url = f"http://search-service:8002/api{endpoint}"
    async with httpx.AsyncClient() as client:
        if method == "POST":
            await client.post(url, json=data)
        elif method == "PUT":
            await client.put(url, json=data)
        elif method == "DELETE":
            await client.delete(url)
```

#### HTTP/JSON
- Protocol: HTTP/1.1 atau HTTP/2
- Data Format: JSON
- Content-Type: application/json
- Status Codes: 200, 201, 400, 404, 500

#### Service Discovery
- Menggunakan Docker Compose service names
- Core Service mengakses Search Service via: `http://search-service:8002`
- Docker Network menangani DNS resolution

### Diagram Arsitektur
```
┌──────────────┐
│   Vue.js     │
│  Frontend    │
│  :3000       │
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────┐
│ Core Service │
│  FastAPI     │
│  :8001       │
└──────┬───────┘
       │
       ├──────────────────┐
       ▼                  ▼
┌──────────────┐  ┌──────────────┐
│   MongoDB    │  │Search Service│
│   :27017     │  │  FastAPI     │
└──────────────┘  │  :8002       │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Elasticsearch│
                  │   :9200      │
                  └──────────────┘

Docker Network: uas_app-network
```

---

## 7. BOOTSTRAP 5

### Apa itu Bootstrap?
Bootstrap adalah CSS framework open-source untuk building responsive, mobile-first websites dan web applications.

### Mengapa Dipilih?
1. **Rapid Development**: Components siap pakai
2. **Responsive**: Mobile-first approach
3. **Consistent Design**: Design system yang konsisten
4. **Well Documented**: Dokumentasi yang excellent
5. **Large Community**: Banyak resources dan tutorials

### Fungsinya
- **CSS Framework**: Styling untuk UI components
- **Grid System**: Responsive layout system
- **Components**: Buttons, forms, tables, modals, cards
- **Utilities**: Spacing, colors, typography
- **JavaScript Plugins**: Dropdowns, modals, carousels

### Kelebihan
✅ Fast development  
✅ Responsive by default  
✅ Consistent design  
✅ Cross-browser compatible  
✅ Large component library  
✅ Easy to customize  
✅ Great documentation  

### Kekurangan
❌ Websites terlihat "Bootstrap-ish"  
❌ Large file size (jika tidak di-optimize)  
❌ Less flexibility dibanding custom CSS  
❌ Overkill untuk simple apps  

### Kenapa Bukan Tailwind CSS?
| Aspek | Bootstrap | Tailwind |
|-------|-----------|----------|
| Approach | Component-based | Utility-first |
| Learning Curve | Mudah | Sedang |
| Customization | Less flexible | Sangat flexible |
| File Size | Larger | Smaller (jika di-purge) |
| Development Speed | Fast | Fast (setelah familiar) |
| Design Consistency | Built-in | Manual |

**Alasan memilih Bootstrap**: Project membutuhkan UI yang cepat dan konsisten tanpa perlu desain custom yang rumit. Bootstrap memberikan components yang siap pakai dengan design yang professional.

---

## 8. AXIOS

### Apa itu Axios?
Axios adalah HTTP client library untuk JavaScript (browser dan Node.js) yang digunakan untuk membuat HTTP requests.

### Mengapa Dipakai?
1. **Promise-based**: Modern async/await syntax
2. **Request/Response Interception**: Bisa modify requests/responses
3. **Automatic JSON Transformation**: Auto parse JSON
4. **Error Handling**: Better error handling
5. **Browser & Node.js Support**: Works di kedua environment

### Fungsinya
```javascript
// GET request
const response = await axios.get('/api/products')

// POST request
const response = await axios.post('/api/products', {
  nama: 'Laptop',
  harga: 5000000
})

// PUT request
const response = await axios.put('/api/products/1', {
  harga: 6000000
})

// DELETE request
const response = await axios.delete('/api/products/1')
```

### Kelebihan
✅ Promise-based API  
✅ Automatic JSON transformation  
✅ Request/response interception  
✅ Better error handling  
✅ Request cancellation  
✅ Timeout configuration  
✅ CSRF protection  

### Kekurangan
❌ Additional dependency  
❌ Larger dibanding fetch API  
❌ Overkill untuk simple apps  

### Kenapa Bukan Fetch API?
| Aspek | Axios | Fetch |
|-------|-------|-------|
| JSON Handling | Automatic | Manual (res.json()) |
| Error Handling | Catch all errors | Only network errors |
| Browser Support | Excellent | Good (IE need polyfill) |
| Interceptors | Built-in | Manual |
| Request Cancel | Easy | AbortController |
| Older Browser | Works | Need polyfill |

**Alasan memilih Axios**: Lebih mudah digunakan, better error handling, dan automatic JSON transformation membuat code lebih bersih.

---

## RINGKASAN TEKNOLOGI

| Teknologi | Kategori | Alasan Pemilihan |
|-----------|----------|------------------|
| Vue.js 3 | Frontend Framework | Mudah dipelajari, performan baik, documentation excellent |
| FastAPI | Backend Framework | Performa tinggi, async support, auto documentation |
| MongoDB | Database | Flexible schema, JSON-like, scalable |
| Elasticsearch | Search Engine | Full-text search cepat, relevance scoring |
| Docker | Containerization | Consistent environment, easy deployment |
| Bootstrap 5 | CSS Framework | Rapid development, responsive, components siap pakai |
| Axios | HTTP Client | Easy to use, better error handling |

---

## TECHNOLOGY STACK DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Vue.js 3 + Bootstrap 5 + Axios                       │ │
│  │  Port: 3000                                           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                           │
│  ┌────────────────────────┐  ┌───────────────────────────┐  │
│  │   Core Service         │  │   Search Service          │  │
│  │   FastAPI              │  │   FastAPI                 │  │
│  │   Port: 8001           │  │   Port: 8002              │  │
│  │   Pydantic v2          │  │   Elasticsearch Client    │  │
│  └────────────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
│  ┌────────────────────────┐  ┌───────────────────────────┐  │
│  │   MongoDB              │  │   Elasticsearch           │  │
│  │   Port: 27017          │  │   Port: 9200              │  │
│  │   Document Store       │  │   Search Engine           │  │
│  └────────────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CONTAINER LAYER                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Docker & Docker Compose                              │ │
│  │  - Containerization                                   │ │
│  │  - Orchestration                                      │ │
│  │  - Volume Management                                  │ │
│  │  - Network Configuration                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘