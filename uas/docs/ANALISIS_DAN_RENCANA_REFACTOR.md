# Analisis Project Lama & Rencana Refactor Microservice

## 1. Analisis Project Lama

### 1.1 Arsitektur Saat Ini (Monolitik CLI)

```
┌─────────────────────────────────────────────────┐
│                  app.py (CLI)                    │
│  ┌─────────────┐  ┌──────────────┐              │
│  │ mongo_      │  │ elastic_    │              │
│  │ service.py  │  │ service.py  │              │
│  └──────┬──────┘  └──────┬───────┘              │
│         │                 │                       │
│  ┌──────┴──────┐  ┌──────┴───────┐              │
│  │   MongoDB   │  │ Elasticsearch │              │
│  └─────────────┘  └──────────────┘              │
│                                                  │
│  compare_service.py  helper.py  config.py        │
└─────────────────────────────────────────────────┘
```

### 1.2 Kelebihan Project Saat Ini
- **Separation of concerns**: Service layer sudah dipisah per database
- **CRUD lengkap**: Insert, Read, Update, Delete sudah terimplementasi
- **Dataset ready**: 12 produk dengan struktur data yang jelas
- **Configuration terpusat**: Semua konfigurasi di `config.py`
- **Logging**: Sudah menggunakan logging Python
- **Error handling**: Exception handling sudah cukup baik

### 1.3 Kekurangan / Yang Perlu Diubah
| Aspek | Masalah | Solusi |
|-------|---------|--------|
| **Arsitektur** | Monolitik CLI | Microservice |
| **Interface** | CLI-only, tidak ada visualisasi | Frontend Web |
| **Komunikasi** | Direct function call | REST API |
| **Deployment** | Manual run Python | Docker + Compose |
| **Dependency** | Manual install pip | Containerized |
| **Config** | Hardcoded di code | Environment variables |
| **Schema** | Tidak ada dokumentasi API | OpenAPI/Swagger |
| **Testing** | Tidak ada test terstruktur | Unit test per service |

### 1.4 Teknis Detail Service Saat Ini

**MongoDB Service** (`mongo_service.py`):
- Fungsi: `insert_banyak()`, `cari_semua()`, `cari_regex()`, `update_data()`, `delete_data()`, `cek_koneksi()`
- Database: `toko_komputer`
- Collection: `produk`
- Search: Regex-based (`$regex`)

**Elasticsearch Service** (`elastic_service.py`):
- Fungsi: `index_banyak()`, `buat_index()`, `cari_match()`, `update_data()`, `delete_data()`, `cek_koneksi()`
- Index: `produk`
- Search: Multi-match query (full-text search)
- Mapping: `_id` (integer), `nama` (text), `kategori` (text), `harga` (integer), `stok` (integer), `spesifikasi` (text)

**Config** (`config.py`):
- MongoDB: `localhost:27017`, database `toko_komputer`, collection `produk`
- Elasticsearch: `localhost:9200`, index `produk`

---

## 2. File yang Dipertahankan

| File | Status | Alasan |
|------|--------|--------|
| `data/products.json` | **DI PERTAHANKAN** | Dataset tetap valid, hanya dipindah ke masing-masing service |
| `app/__init__.py` | **DI HAPUS** | Struktur package berubah total |
| `app/config.py` | **DI REFACTOR** | Dipindah ke environment variable + docker-compose |
| `app/mongo_service.py` | **DI REFACTOR** | Logika CRUD dipertahankan, tapi dipisah ke Core Service |
| `app/elastic_service.py` | **DI REFACTOR** | Logika CRUD dipertahankan, tapi dipisah ke Search Service |
| `app/compare_service.py` | **DI REFACTOR** | Logika perbandingan dijadikan endpoint REST API |
| `app/helper.py` | **DI REFACTOR** | Fungsi formatting dipindah ke masing-masing service sesuai kebutuhan |
| `app.py` | **DI HAPUS** | CLI diganti dengan REST API + Frontend |
| `requirements.txt` | **DI REFACTOR** | Dipisah per service (masing-masing punya dependencies sendiri) |

---

## 3. File yang Direfactor

### 3.1 `app/config.py` → Environment Variables
- Semua hardcoded config diubah menjadi environment variable
- Dibaca via `os.getenv()` di masing-masing service
- Default value untuk development

**Mapping Config:**
```
Config Lama              → Environment Variable Baru
─────────────────────────────────────────────────
MONGO_HOST               → MONGO_HOST
MONGO_PORT               → MONGO_PORT  
MONGO_DB_NAME            → MONGO_DB_NAME
MONGO_COLLECTION_NAME    → MONGO_COLLECTION_NAME
ELASTIC_HOST             → ELASTIC_HOST
ELASTIC_PORT             → ELASTIC_PORT
ELASTIC_INDEX_NAME       → ELASTIC_INDEX_NAME
```

### 3.2 `app/mongo_service.py` → Core Service (Python/FastAPI)
- Logika CRUD dipertahankan 80%
- Ditambahkan REST API wrapper menggunakan FastAPI
- Fungsi `cari_regex()` dipertahankan sebagai endpoint `GET /api/products/search?q=keyword`
- Fungsi `insert_banyak()` menjadi endpoint `POST /api/products/seed`
- Semua fungsi CRUD lainnya menjadi endpoint REST standar

### 3.3 `app/elastic_service.py` → Search Service (Python/FastAPI)
- Logika indexing dan search dipertahankan 80%
- Ditambahkan REST API wrapper menggunakan FastAPI
- Fungsi `cari_match()` menjadi endpoint `GET /api/search?q=keyword`
- Fungsi sync data dari Core Service via REST call atau message queue

### 3.4 `app/compare_service.py` → API Endpoint di Core Service
- Logika perbandingan dijadikan endpoint khusus
- Core Service memanggil Search Service via HTTP
- Endpoint: `GET /api/compare?q=keyword`

### 3.5 `app/helper.py` → Utility per Service
- `format_harga()` → dipindah ke frontend (client-side formatting)
- `hitung_waktu()` → dipindah ke middleware atau dihapus (tidak relevan untuk REST)
- `cetak_*` functions → dihapus (diganti response JSON)
- `input_*` functions → dihapus (diganti request body/params)

### 3.6 `app.py` → Diganti dengan FastAPI Router
- Semua fungsi menu (insert, search, update, delete, bandingkan) → endpoint REST
- Tidak ada CLI, hanya REST API + Frontend

---

## 4. Arsitektur Baru (Microservice)

```
┌─────────────────────────────────────────────────────────┐
│                     DOCKER COMPOSE                       │
│                                                          │
│  ┌─────────────┐    ┌────────────────────────────┐      │
│  │   Frontend  │───▶│     Core Service           │      │
│  │   (React/   │    │  - FastAPI Python          │      │
│  │    Next.js) │◀───│  - CRUD MongoDB            │      │
│  │   :3000     │    │  - Product API             │      │
│  └──────┬──────┘    │  - Compare API             │      │
│         │           │  - Seed Data               │      │
│         │           └────────┬───────────────────┘      │
│         │                    │ HTTP REST                 │
│         │           ┌───────▼───────────────────┐       │
│         │           │     Search Service        │       │
│         └───────────│  - FastAPI Python          │       │
│                     │  - Full-text Search ES     │       │
│                     │  - Search API              │       │
│                     └────────┬───────────────────┘       │
│                              │                           │
│              ┌───────────────┴──────────────┐            │
│              │                              │            │
│     ┌────────▼────────┐          ┌─────────▼────────┐   │
│     │    MongoDB       │          │  Elasticsearch   │   │
│     │    :27017        │          │  :9200           │   │
│     └─────────────────┘          └──────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 4.1 Alur Data
```
Client (Browser)          Core Service             Search Service
      │                       │                         │
      │  GET /api/products    │                         │
      │──────────────────────▶│                         │
      │◀──────────────────────│                         │
      │                       │                         │
      │  GET /api/search?q=X  │                         │
      │───────────────────────│────────────────────────▶│
      │◀──────────────────────│◀────────────────────────│
      │                       │                         │
      │  GET /api/compare?q=X │                         │
      │──────────────────────▶│  GET /api/search?q=X    │
      │                       │────────────────────────▶│
      │◀──────────────────────│◀────────────────────────│
      │                       │                         │
      │  POST /api/products   │                         │
      │  (seed data)          │  POST /api/search/sync  │
      │──────────────────────▶│────────────────────────▶│
      │◀──────────────────────│◀────────────────────────│
```

### 4.2 Inter-Service Communication
- **Synchronous**: Core Service → Search Service via HTTP REST
- **Data Flow**: Saat seed/update/delete, Core Service mengirim request ke Search Service untuk sinkronisasi
- **Format**: JSON

---

## 5. Struktur Folder Baru

```
uas/
├── docker-compose.yml              # Orchestrator semua service
├── .env                            # Environment variables
├── .gitignore
├── README.md
│
├── core-service/                   # Core Service (MongoDB CRUD)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Baca environment variables
│   │   ├── database.py             # MongoDB connection manager
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── product.py          # Pydantic models / schema
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── product_repository.py  # MongoDB operations (refactor dari mongo_service.py)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── product_service.py     # Business logic
│   │   │   └── compare_service.py     # Compare logic (refactor dari compare_service.py)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── products.py            # Endpoints CRUD produk
│   │   │   └── compare.py             # Endpoint compare
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py             # Utility functions sisa dari helper.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_products.py
│
├── search-service/                 # Search Service (Elasticsearch)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Baca environment variables
│   │   ├── database.py             # Elasticsearch connection manager
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── product.py          # Pydantic models / schema
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── search_repository.py   # ES operations (refactor dari elastic_service.py)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── search_service.py      # Business logic
│   │   └── api/
│   │       ├── __init__.py
│   │       └── search.py              # Endpoints search
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_search.py
│
├── frontend/                       # Frontend Web
│   ├── Dockerfile
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js/jsx
│   │   ├── index.js/jsx
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   ├── Products/
│   │   │   │   ├── ProductList.jsx
│   │   │   │   ├── ProductCard.jsx
│   │   │   │   ├── ProductForm.jsx
│   │   │   │   └── ProductDetail.jsx
│   │   │   ├── Search/
│   │   │   │   ├── SearchBar.jsx
│   │   │   │   └── SearchResults.jsx
│   │   │   ├── Compare/
│   │   │   │   └── CompareResults.jsx
│   │   │   └── Common/
│   │   │       ├── Loading.jsx
│   │   │       ├── Error.jsx
│   │   │       └── Table.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ProductsPage.jsx
│   │   │   ├── SearchPage.jsx
│   │   │   └── ComparePage.jsx
│   │   ├── services/
│   │   │   └── api.js              # Axios/fetch ke backend
│   │   └── styles/
│   │       └── global.css
│   └── ...
│
├── data/
│   └── products.json               # Dataset (tetap dipertahankan)
│
└── docs/
    ├── ANALISIS_DAN_RENCANA_REFACTOR.md
    ├── SKPL.md                     # Spesifikasi Kebutuhan Perangkat Lunak
    └── API.md                      # Dokumentasi API
```

---

## 6. Daftar Endpoint REST API

### 6.1 Core Service (`http://localhost:8001`)

| Method | Endpoint | Deskripsi | Status Code |
|--------|----------|-----------|-------------|
| **GET** | `/api` | Root / health check | 200 |
| **GET** | `/api/products` | Ambil semua produk | 200 |
| **GET** | `/api/products/{id}` | Ambil produk by ID | 200 / 404 |
| **POST** | `/api/products` | Tambah produk baru | 201 / 400 |
| **POST** | `/api/products/seed` | Seed dataset dari products.json | 201 |
| **PUT** | `/api/products/{id}` | Update produk | 200 / 404 |
| **DELETE** | `/api/products/{id}` | Hapus produk | 200 / 404 |
| **GET** | `/api/products/search` | Cari produk di MongoDB (regex) | 200 |
| **GET** | `/api/compare` | Bandingkan MongoDB vs ES | 200 |
| **GET** | `/api/compare/history` | Riwayat perbandingan | 200 |
| **GET** | `/docs` | Swagger UI (FastAPI auto) | 200 |

### 6.2 Search Service (`http://localhost:8002`)

| Method | Endpoint | Deskripsi | Status Code |
|--------|----------|-----------|-------------|
| **GET** | `/api` | Root / health check | 200 |
| **GET** | `/api/search` | Full-text search via ES | 200 |
| **POST** | `/api/search/sync` | Sinkronisasi data dari Core Service | 201 |
| **PUT** | `/api/search/sync/{id}` | Update single document di ES | 200 |
| **DELETE** | `/api/search/sync/{id}` | Hapus document dari ES | 200 |
| **GET** | `/api/search/stats` | Statistik index ES | 200 |
| **GET** | `/docs` | Swagger UI (FastAPI auto) | 200 |

### 6.3 Query Parameters

**Search Endpoint:**
```
GET /api/products/search?q=keyboard&page=1&limit=10
GET /api/search?q=keyboard&page=1&limit=10
GET /api/compare?q=keyboard
```

**Response Format (Standar):**
```json
{
  "status": "success",
  "message": "...",
  "data": {
    // payload sesuai endpoint
  },
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 12
  }
}
```

### 6.4 Error Response Format
```json
{
  "status": "error",
  "message": "Product not found",
  "error_code": "NOT_FOUND",
  "details": null
}
```

---

## 7. Roadmap Implementasi

### Phase 1: Foundation (Hari 1-2)
- [ ] Setup struktur folder microservice
- [ ] Init `core-service` dengan FastAPI
- [ ] Init `search-service` dengan FastAPI
- [ ] Setup MongoDB connection di core-service (refactor dari `mongo_service.py`)
- [ ] Setup Elasticsearch connection di search-service (refactor dari `elastic_service.py`)
- [ ] Pindahkan `products.json` ke masing-masing service / tetap di `data/`

### Phase 2: Core Service REST API (Hari 3-4)
- [ ] Implementasi endpoint `GET /api/products` (refactor `cari_semua()`)
- [ ] Implementasi endpoint `GET /api/products/{id}` (ambil by ID)
- [ ] Implementasi endpoint `POST /api/products/seed` (refactor `insert_banyak()`)
- [ ] Implementasi endpoint `POST /api/products` (tambah single product)
- [ ] Implementasi endpoint `PUT /api/products/{id}` (refactor `update_data()`)
- [ ] Implementasi endpoint `DELETE /api/products/{id}` (refactor `delete_data()`)
- [ ] Implementasi endpoint `GET /api/products/search` (refactor `cari_regex()`)
- [ ] Implementasi Pydantic models / request-response schema
- [ ] Error handling & validasi

### Phase 3: Search Service REST API (Hari 5-6)
- [ ] Implementasi endpoint `GET /api/search` (refactor `cari_match()`)
- [ ] Implementasi endpoint `POST /api/search/sync` (refactor `index_banyak()`)
- [ ] Implementasi endpoint `PUT /api/search/sync/{id}` (refactor `update_data()`)
- [ ] Implementasi endpoint `DELETE /api/search/sync/{id}` (refactor `delete_data()`)
- [ ] Implementasi mapping index ES otomatis (refactor `buat_index()`)
- [ ] Health check & connection validation

### Phase 4: Compare & Integration (Hari 7-8)
- [ ] Refactor `compare_service.py` ke endpoint `GET /api/compare`
- [ ] Implementasi inter-service communication (Core → Search via HTTP)
- [ ] Implementasi sinkronisasi data antara Core Service dan Search Service
- [ ] Handle error dan timeout untuk interservice call
- [ ] Testing integrasi antar service

### Phase 5: Frontend Web (Hari 9-11)
- [ ] Setup React/Next.js project
- [ ] Implementasi halaman Home (dashboard)
- [ ] Implementasi halaman Products (list + CRUD)
- [ ] Implementasi halaman Search (full-text search)
- [ ] Implementasi halaman Compare (perbandingan)
- [ ] Integrasi dengan Core Service dan Search Service API
- [ ] UI/UX styling

### Phase 6: Docker & Deployment (Hari 12-13)
- [ ] Buat `Dockerfile` untuk core-service
- [ ] Buat `Dockerfile` untuk search-service
- [ ] Buat `Dockerfile` untuk frontend
- [ ] Buat `docker-compose.yml` (semua service + database)
- [ ] Setup network antar service di Docker
- [ ] Environment variables via `.env`
- [ ] Volume mounting untuk data persistence

### Phase 7: Dokumentasi & SKPL (Hari 14-15)
- [ ] Buat SKPL (Spesifikasi Kebutuhan Perangkat Lunak)
- [ ] Dokumentasi API dengan OpenAPI/Swagger
- [ ] README.md dengan cara menjalankan
- [ ] Dokumentasi arsitektur

---

## 8. Ringkasan Perubahan

### Dari Project Lama → Project Baru

| Komponen | Sebelum | Sesudah |
|----------|---------|---------|
| **Entry Point** | `app.py` (CLI) | `main.py` (FastAPI) |
| **Database Access** | Direct function call | REST API endpoints |
| **Frontend** | Tidak ada | React/Next.js Web App |
| **MongoDB** | Service dalam satu package | Core Service (container sendiri) |
| **Elasticsearch** | Service dalam satu package | Search Service (container sendiri) |
| **Deployment** | `python app.py` | `docker-compose up` |
| **Config** | Hardcoded di `config.py` | Environment variables |
| **Dataset** | `data/products.json` | Tetap dipertahankan |
| **Logika CRUD** | `mongo_service.py` | `repositories/product_repository.py` |
| **Logika Search** | `elastic_service.py` | `repositories/search_repository.py` |
| **Logika Compare** | `compare_service.py` | `services/compare_service.py` |
| **Helper** | `helper.py` | Terdistribusi sesuai kebutuhan |

### Dependency Baru (tambahan)
```
# core-service
fastapi==0.104.0
uvicorn==0.24.0
pymongo==4.6.1
pydantic==2.5.0
httpx==0.25.0      # Untuk interservice communication
python-dotenv==1.0.0

# search-service
fastapi==0.104.0
uvicorn==0.24.0
elasticsearch==7.13.4
pydantic==2.5.0
python-dotenv==1.0.0

# frontend
react
axios / fetch
react-router-dom