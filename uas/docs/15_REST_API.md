# REST API DOCUMENTATION

## Overview
Bagian ini mendokumentasikan seluruh REST API endpoints yang tersedia dalam sistem ini. Dokumentasi ini mencakup Core Service (CRUD operations) dan Search Service (search operations).

---

## Base URLs

```
Core Service:      http://localhost:8001/api
Search Service:    http://localhost:8002/api
```

---

## 1. Core Service API (Port 8001)

### Base URL
```
http://localhost:8001/api
```

### 1.1 Products Endpoints

#### GET /api/products
Mengambil semua produk dari MongoDB.

**Request:**
```bash
GET http://localhost:8001/api/products
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Ditemukan 12 produk",
  "data": [
    {
      "_id": 1,
      "nama": "Laptop Asus ROG Zephyrus G14",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
    },
    {
      "_id": 2,
      "nama": "iPhone 15 Pro Max",
      "kategori": "Phone",
      "harga": 25000000,
      "stok": 8,
      "spesifikasi": "A17 Pro, 256GB, Titanium"
    }
  ],
  "total": 12
}
```

**Error Response (503):**
```json
{
  "detail": "MongoDB tidak tersedia"
}
```

---

#### GET /api/products/{product_id}
Mengambil satu produk berdasarkan ID.

**Request:**
```bash
GET http://localhost:8001/api/products/1
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Produk ditemukan",
  "data": {
    "_id": 1,
    "nama": "Laptop Asus ROG Zephyrus G14",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
  }
}
```

**Error Response (404):**
```json
{
  "detail": "Produk dengan ID 999 tidak ditemukan"
}
```

---

#### POST /api/products
Membuat produk baru.

**Request:**
```bash
POST http://localhost:8001/api/products
Content-Type: application/json

{
  "_id": 13,
  "nama": "MacBook Pro M3",
  "kategori": "Laptop",
  "harga": 35000000,
  "stok": 5,
  "spesifikasi": "Apple M3, RAM 18GB, SSD 512GB"
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Produk ID 13 berhasil dibuat",
  "data": {
    "_id": 13,
    "nama": "MacBook Pro M3",
    "kategori": "Laptop",
    "harga": 35000000,
    "stok": 5,
    "spesifikasi": "Apple M3, RAM 18GB, SSD 512GB"
  }
}
```

**Error Response (400) - Duplicate:**
```json
{
  "detail": "Produk dengan ID 13 sudah ada"
}
```

**Error Response (422) - Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "harga"],
      "msg": "Input should be greater than or equal to 0",
      "type": "greater_than_equal"
    }
  ]
}
```

---

#### PUT /api/products/{product_id}
Mengupdate produk yang ada.

**Request:**
```bash
PUT http://localhost:8001/api/products/1
Content-Type: application/json

{
  "nama": "Laptop Asus ROG Zephyrus G14 (Updated)",
  "harga": 19999000,
  "stok": 12
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil diupdate",
  "data": {
    "_id": 1,
    "nama": "Laptop Asus ROG Zephyrus G14 (Updated)",
    "kategori": "Laptop",
    "harga": 19999000,
    "stok": 12,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
  }
}
```

**Error Response (404):**
```json
{
  "detail": "Produk dengan ID 999 tidak ditemukan"
}
```

**Error Response (400):**
```json
{
  "detail": "Tidak ada data yang diupdate"
}
```

---

#### DELETE /api/products/{product_id}
Menghapus produk.

**Request:**
```bash
DELETE http://localhost:8001/api/products/1
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil dihapus",
  "data": null
}
```

**Error Response (404):**
```json
{
  "detail": "Produk dengan ID 999 tidak ditemukan"
}
```

---

### 1.2 Seed Endpoint

#### POST /api/products/seed
Mengisi database dengan data sample dari JSON file.

**Request:**
```bash
POST http://localhost:8001/api/products/seed
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Berhasil seed 12 produk ke MongoDB dan Elasticsearch",
  "data": [
    {
      "_id": 1,
      "nama": "Laptop Asus ROG Zephyrus G14",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
    },
    ...
  ],
  "total": 12
}
```

**Error Response (503):**
```json
{
  "detail": "MongoDB tidak tersedia"
}
```

---

### 1.3 Health Check

#### GET /health
Mengecek status Core Service.

**Request:**
```bash
GET http://localhost:8001/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "core-service"
}
```

---

## 2. Search Service API (Port 8002)

### Base URL
```
http://localhost:8002/api
```

### 2.1 Search Endpoints

#### GET /api/search
Mencari produk menggunakan full-text search.

**Request:**
```bash
GET http://localhost:8002/api/search?q=laptop gaming
```

**Query Parameters:**
- `q` (required): Kata kunci pencarian

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Ditemukan 3 hasil untuk 'laptop gaming'",
  "data": [
    {
      "nama": "Laptop Gaming Asus ROG",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
    },
    {
      "nama": "Laptop Gaming Terbaik",
      "kategori": "Laptop",
      "harga": 15999000,
      "stok": 8,
      "spesifikasi": "Intel i7, RAM 8GB, SSD 256GB"
    },
    {
      "nama": "Gaming Laptop Acer",
      "kategori": "Laptop",
      "harga": 12999000,
      "stok": 12,
      "spesifikasi": "AMD Ryzen 5, RAM 8GB, SSD 512GB"
    }
  ],
  "total": 3,
  "keyword": "laptop gaming"
}
```

**Response (200 OK) - No Results:**
```json
{
  "status": "success",
  "message": "Ditemukan 0 hasil untuk 'xyz123'",
  "data": [],
  "total": 0,
  "keyword": "xyz123"
}
```

**Error Response (503):**
```json
{
  "detail": "Elasticsearch tidak tersedia"
}
```

---

#### GET /api/stats
Mendapatkan statistik Elasticsearch index.

**Request:**
```bash
GET http://localhost:8002/api/stats
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "status": "connected",
    "index": "produk",
    "document_count": 12,
    "size_in_bytes": 8162
  }
}
```

**Error Response (503):**
```json
{
  "detail": "Elasticsearch tidak tersedia"
}
```

---

### 2.2 Sync Endpoints (Internal)

#### POST /api/sync
Bulk sync - menyinkronisasi multiple products ke Elasticsearch.

**Request:**
```bash
POST http://localhost:8002/api/sync
Content-Type: application/json

{
  "products": [
    {
      "_id": 1,
      "nama": "Laptop Asus",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB"
    },
    ...
  ]
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Berhasil sinkronisasi 12 produk ke Elasticsearch",
  "total": 12
}
```

**Error Response (400):**
```json
{
  "detail": "Tidak ada data produk untuk disinkronisasi"
}
```

---

#### POST /api/sync/single
Single product sync - menyinkronisasi satu product ke Elasticsearch.

**Request:**
```bash
POST http://localhost:8002/api/sync/single
Content-Type: application/json

{
  "_id": 13,
  "nama": "MacBook Pro M3",
  "kategori": "Laptop",
  "harga": 35000000,
  "stok": 5,
  "spesifikasi": "Apple M3, RAM 18GB, SSD 512GB"
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Produk ID 13 berhasil disinkronisasi",
  "total": 1
}
```

---

#### PUT /api/sync/{product_id}
Update product di Elasticsearch.

**Request:**
```bash
PUT http://localhost:8002/api/sync/1
Content-Type: application/json

{
  "nama": "Laptop Asus ROG Zephyrus G14 (Updated)",
  "harga": 19999000
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil diupdate di Elasticsearch",
  "total": 1
}
```

**Error Response (404):**
```json
{
  "detail": "Produk ID 999 tidak ditemukan di Elasticsearch"
}
```

---

#### DELETE /api/sync/{product_id}
Delete product dari Elasticsearch.

**Request:**
```bash
DELETE http://localhost:8002/api/sync/1
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil dihapus dari Elasticsearch",
  "total": 1
}
```

**Error Response (404):**
```json
{
  "detail": "Produk ID 999 tidak ditemukan di Elasticsearch"
}
```

---

### 2.3 Health Check

#### GET /health
Mengecek status Search Service.

**Request:**
```bash
GET http://localhost:8002/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "search-service"
}
```

---

## 3. Data Models

### 3.1 ProductCreateSchema
```json
{
  "_id": 1,
  "nama": "Laptop Asus ROG",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB"
}
```

**Field Descriptions:**
- `_id` (integer, required): Unique product ID
- `nama` (string, required): Product name
- `kategori` (string, required): Product category
- `harga` (integer, required, min=0): Product price
- `stok` (integer, required, min=0): Stock quantity
- `spesifikasi` (string, required): Product specifications

---

### 3.2 ProductUpdateSchema
```json
{
  "nama": "Updated Product Name",
  "kategori": "Laptop",
  "harga": 19999000,
  "stok": 20,
  "spesifikasi": "Updated specifications"
}
```

**Field Descriptions:**
- `nama` (string, optional): Product name
- `kategori` (string, optional): Product category
- `harga` (integer, optional, min=0): Product price
- `stok` (integer, optional, min=0): Stock quantity
- `spesifikasi` (string, optional): Product specifications

**Note**: All fields are optional. Only provided fields will be updated.

---

### 3.3 ProductResponse
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil dibuat",
  "data": {
    "_id": 1,
    "nama": "Laptop Asus ROG",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB"
  }
}
```

---

### 3.4 ProductListResponse
```json
{
  "status": "success",
  "message": "Ditemukan 12 produk",
  "data": [
    {
      "_id": 1,
      "nama": "Laptop Asus ROG",
      ...
    },
    ...
  ],
  "total": 12
}
```

---

### 3.5 SearchResponse
```json
{
  "status": "success",
  "message": "Ditemukan 3 hasil untuk 'laptop gaming'",
  "data": [
    {
      "nama": "Laptop Gaming Asus",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB"
    },
    ...
  ],
  "total": 3,
  "keyword": "laptop gaming"
}
```

---

### 3.6 SyncResponse
```json
{
  "status": "success",
  "message": "Produk ID 1 berhasil disinkronisasi",
  "total": 1
}
```

---

## 4. Error Codes

### 4.1 HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| **200** | OK | Successful GET, PUT, DELETE |
| **201** | Created | Successful POST |
| **400** | Bad Request | Validation error, duplicate data |
| **404** | Not Found | Product not found |
| **422** | Unprocessable Entity | Validation error (Pydantic) |
| **500** | Internal Server Error | Server error |
| **503** | Service Unavailable | Database/Elasticsearch unavailable |

### 4.2 Error Response Format

```json
{
  "detail": "Error message here"
}
```

**Example Errors:**

**400 Bad Request:**
```json
{
  "detail": "Produk dengan ID 1 sudah ada"
}
```

**404 Not Found:**
```json
{
  "detail": "Produk dengan ID 999 tidak ditemukan"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "harga"],
      "msg": "Input should be greater than or equal to 0",
      "type": "greater_than_equal"
    }
  ]
}
```

**503 Service Unavailable:**
```json
{
  "detail": "MongoDB tidak tersedia"
}
```

---

## 5. API Testing Examples

### 5.1 Using cURL

#### Create Product
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
```

#### Get All Products
```bash
curl http://localhost:8001/api/products
```

#### Get Single Product
```bash
curl http://localhost:8001/api/products/1
```

#### Update Product
```bash
curl -X PUT http://localhost:8001/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Updated Product",
    "harga": 200000
  }'
```

#### Delete Product
```bash
curl -X DELETE http://localhost:8001/api/products/1
```

#### Search Products
```bash
curl "http://localhost:8002/api/search?q=laptop"
```

#### Get Stats
```bash
curl http://localhost:8002/api/stats
```

---

### 5.2 Using PowerShell (Windows)

#### Create Product
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/products" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"_id": 99, "nama": "Test Product", "kategori": "Test", "harga": 100000, "stok": 10, "spesifikasi": "Test"}'
```

#### Get All Products
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/api/products" -Method GET
```

#### Search Products
```powershell
Invoke-RestMethod -Uri "http://localhost:8002/api/search?q=laptop" -Method GET
```

---

### 5.3 Using Axios (JavaScript)

```javascript
import axios from 'axios'

const API_BASE = 'http://localhost:8001/api'
const SEARCH_BASE = 'http://localhost:8002/api'

// Create Product
async function createProduct(product) {
  const response = await axios.post(`${API_BASE}/products`, product)
  return response.data
}

// Get All Products
async function getAllProducts() {
  const response = await axios.get(`${API_BASE}/products`)
  return response.data
}

// Get Single Product
async function getProduct(id) {
  const response = await axios.get(`${API_BASE}/products/${id}`)
  return response.data
}

// Update Product
async function updateProduct(id, data) {
  const response = await axios.put(`${API_BASE}/products/${id}`, data)
  return response.data
}

// Delete Product
async function deleteProduct(id) {
  const response = await axios.delete(`${API_BASE}/products/${id}`)
  return response.data
}

// Search Products
async function searchProducts(query) {
  const response = await axios.get(`${SEARCH_BASE}/search`, {
    params: { q: query }
  })
  return response.data
}

// Seed Data
async function seedProducts() {
  const response = await axios.post(`${API_BASE}/products/seed`)
  return response.data
}
```

---

## 6. API Flow Diagrams

### 6.1 CRUD Flow

```
CREATE Product:
POST /api/products
  ↓
MongoDB: insert_one()
  ↓
Async: POST /api/sync/single
  ↓
Elasticsearch: index()
  ↓
Return 201 Created

READ Products:
GET /api/products
  ↓
MongoDB: find({})
  ↓
Return 200 OK

READ Single Product:
GET /api/products/1
  ↓
MongoDB: find_one({_id: 1})
  ↓
Return 200 OK

UPDATE Product:
PUT /api/products/1
  ↓
MongoDB: update_one()
  ↓
Async: PUT /api/sync/1
  ↓
Elasticsearch: update()
  ↓
Return 200 OK

DELETE Product:
DELETE /api/products/1
  ↓
MongoDB: delete_one()
  ↓
Async: DELETE /api/sync/1
  ↓
Elasticsearch: delete()
  ↓
Return 200 OK
```

### 6.2 Search Flow

```
SEARCH Products:
GET /api/search?q=laptop
  ↓
Elasticsearch: search()
  ↓
Inverted Index Lookup
  ↓
Calculate Scores (BM25)
  ↓
Sort by Relevance
  ↓
Return 200 OK with results
```

### 6.3 Sync Flow

```
BULK SYNC:
POST /api/sync
  ↓
Elasticsearch: delete index
  ↓
Elasticsearch: create index
  ↓
Elasticsearch: index many
  ↓
Return 201 Created

SINGLE SYNC:
POST /api/sync/single
  ↓
Elasticsearch: index()
  ↓
Return 201 Created

UPDATE SYNC:
PUT /api/sync/1
  ↓
Elasticsearch: update()
  ↓
Return 200 OK

DELETE SYNC:
DELETE /api/sync/1
  ↓
Elasticsearch: delete()
  ↓
Return 200 OK
```

---

## 7. Rate Limiting & Best Practices

### 7.1 Rate Limiting
Currently no rate limiting implemented. For production, consider:
- API Gateway (Nginx/Kong)
- Token bucket algorithm
- Per-user limits

### 7.2 Best Practices

#### For API Consumers
1. **Always check response status code**
2. **Handle errors gracefully**
3. **Use debouncing for search** (300ms recommended)
4. **Cache frequent requests** (future enhancement)
5. **Retry failed requests** with exponential backoff

#### For API Developers
1. **Validate all inputs** (Pydantic handles this)
2. **Return appropriate HTTP status codes**
3. **Log all requests** for debugging
4. **Monitor API performance**
5. **Version your API** (future: /api/v1/products)

---

## 8. Swagger Documentation

### Access Swagger UI
```
Core Service: http://localhost:8001/docs
Search Service: http://localhost:8002/docs
```

### Features
- Interactive API testing
- Request/Response examples
- Schema definitions
- Try-it-out functionality

---

## 9. Postman Collection

### Import Collection
Create a Postman collection with these requests:

**Collection Name:** Product Management API

**Folders:**
1. **Products (Core Service)**
   - GET All Products
   - GET Product by ID
   - CREATE Product
   - UPDATE Product
   - DELETE Product
   - Seed Data

2. **Search (Search Service)**
   - Search Products
   - Get Stats

3. **Sync (Internal)**
   - Bulk Sync
   - Single Sync
   - Update Sync
   - Delete Sync

---

## Summary

### Core Service Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/products | Get all products |
| GET | /api/products/{id} | Get product by ID |
| POST | /api/products | Create product |
| PUT | /api/products/{id} | Update product |
| DELETE | /api/products/{id} | Delete product |
| POST | /api/products/seed | Seed data |
| GET | /health | Health check |

### Search Service Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/search | Search products |
| GET | /api/stats | Get index stats |
| POST | /api/sync | Bulk sync |
| POST | /api/sync/single | Single sync |
| PUT | /api/sync/{id} | Update sync |
| DELETE | /api/sync/{id} | Delete sync |
| GET | /health | Health check |

### Total Endpoints: 13
- Core Service: 7 endpoints
- Search Service: 6 endpoints