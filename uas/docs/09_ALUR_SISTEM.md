# ALUR SISTEM

## Overview
Bagian ini menjelaskan alur sistem secara keseluruhan, dari perspektif user hingga level database. Setiap operasi dijelaskan dengan detail untuk memberikan pemahaman yang komprehensif tentang bagaimana sistem bekerja.

---

## System Flow Overview

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. HTTP Request
       ▼
┌─────────────────────┐
│   Frontend          │
│   (Vue.js)          │
│   Port: 3000        │
└──────┬──────────────┘
       │
       │ 2. API Call (Axios)
       ▼
┌─────────────────────┐
│   Core Service      │
│   (FastAPI)         │
│   Port: 8001        │
└──────┬──────────────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌──────────────┐   ┌──────────────┐
│   MongoDB    │   │Search Service│
│   Port:27017 │   │   Port:8002  │
└──────────────┘   └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Elasticsearch│
                    │   Port:9200  │
                    └──────────────┘
```

---

## 1. Application Startup Flow

### Docker Compose Startup
```bash
# User runs command
docker-compose up -d

# Docker Compose starts services in order:
1. Create network (uas_app-network)
2. Create volumes (mongodb_data, elasticsearch_data)
3. Start MongoDB container
4. Wait for MongoDB health check
5. Start Elasticsearch container
6. Wait for Elasticsearch health check
7. Start Core Service container
8. Start Search Service container
9. Start Frontend container
```

### Service Initialization

#### MongoDB Initialization
```
Container Start
    ↓
Load MongoDB binary
    ↓
Mount volume (mongodb_data)
    ↓
Start mongod process
    ↓
Listen on port 27017
    ↓
Health check: mongosh --eval "db.adminCommand('ping')"
    ↓
Status: Healthy ✓
```

#### Elasticsearch Initialization
```
Container Start
    ↓
Set environment variables
    ↓
Load Elasticsearch binary
    ↓
Mount volume (elasticsearch_data)
    ↓
Start elasticsearch process
    ↓
Initialize cluster (single-node)
    ↓
Listen on port 9200
    ↓
Health check: curl http://localhost:9200
    ↓
Status: Healthy ✓
```

#### Core Service Initialization
```
Container Start
    ↓
Load Python environment
    ↓
Install dependencies (FastAPI, PyMongo, httpx)
    ↓
Load application code
    ↓
Initialize FastAPI app
    ↓
Connect to MongoDB
    ↓
Connect to Search Service (optional)
    ↓
Start Uvicorn server
    ↓
Listen on port 8001
    ↓
Status: Running ✓
```

#### Search Service Initialization
```
Container Start
    ↓
Load Python environment
    ↓
Install dependencies (FastAPI, Elasticsearch client)
    ↓
Load application code
    ↓
Initialize FastAPI app
    ↓
Connect to Elasticsearch
    ↓
Create index if not exists
    ↓
Start Uvicorn server
    ↓
Listen on port 8002
    ↓
Status: Running ✓
```

#### Frontend Initialization
```
Container Start
    ↓
Load Node.js environment
    ↓
Install dependencies (Vue.js, Bootstrap, Axios)
    ↓
Build application (npm run build)
    ↓
Start Nginx server
    ↓
Serve static files
    ↓
Listen on port 3000
    ↓
Status: Running ✓
```

---

## 2. CRUD Operations Flow

### 2.1 CREATE Product

#### Flow Diagram
```
┌──────────┐
│  User    │
│  Action: │
│  Create  │
└────┬─────┘
     │
     │ 1. Fill form & submit
     ▼
┌─────────────────────┐
│   Frontend          │
│   (Vue.js)          │
│                     │
│  - Validate input   │
│  - Create JSON      │
└────┬────────────────┘
     │
     │ 2. POST /api/products
     │    {_id: 1, nama: "Laptop", ...}
     ▼
┌─────────────────────┐
│   Core Service      │
│   (FastAPI)         │
│                     │
│  - Validate schema  │
│  - Check duplicate  │
└────┬────────────────┘
     │
     │ 3. insert_one()
     ▼
┌─────────────────────┐
│   MongoDB           │
│                     │
│  - Insert document  │
│  - Return _id       │
└────┬────────────────┘
     │
     │ 4. Success
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Create sync task │
│  - Return response  │
└────┬────────────────┘
     │
     │ 5. (Async) POST /api/sync/single
     │    {_id: 1, nama: "Laptop", ...}
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Index document   │
│  - Refresh index    │
└────┬────────────────┘
     │
     │ 6. 201 Created
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Complete sync    │
└────┬────────────────┘
     │
     │ 7. 201 Created
     │    {message: "Produk ID 1 berhasil dibuat", ...}
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Show success     │
│  - Refresh list     │
│  - Clear form       │
└────┬────────────────┘
     │
     │ 8. Display updated UI
     ▼
┌──────────┐
│  User    │
│  Sees    │
│  new     │
│  product │
└──────────┘
```

#### Detailed Steps

**Step 1: Frontend**
```javascript
// User fills form
const product = {
  _id: 1,
  nama: "Laptop Asus ROG",
  kategori: "Laptop",
  harga: 18999000,
  stok: 15,
  spesifikasi: "AMD Ryzen 9, RAM 16GB"
}

// Send POST request
const response = await axios.post('/api/products', product)
```

**Step 2: Core Service - Validation**
```python
# Receive request
@router.post("/products")
async def create_product(product: ProductCreateSchema):
    # Pydantic validates:
    # - id is required (int)
    # - nama is required (str)
    # - harga >= 0
    # - stok >= 0
    
    # Check duplicate
    existing = mongo.cari_by_id(product.id)
    if existing:
        raise HTTPException(400, "Produk sudah ada")
```

**Step 3: Core Service - MongoDB Insert**
```python
    # Convert to dict with alias
    produk_dict = product.model_dump(by_alias=True)
    # Result: {"_id": 1, "nama": "Laptop", ...}
    
    # Insert to MongoDB
    result = mongo.insert_satu(produk_dict)
    # MongoDB returns: ObjectId("...")
```

**Step 4: MongoDB - Insert Operation**
```javascript
// MongoDB receives
db.products.insertOne({
  "_id": 1,
  "nama": "Laptop Asus ROG",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": "AMD Ryzen 9, RAM 16GB"
})

// MongoDB stores document
// Returns: {acknowledged: true, insertedId: 1}
```

**Step 5: Core Service - Sync (Async)**
```python
    # Create background task (fire-and-forget)
    asyncio.create_task(
        sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
    )
    
    # Immediately return response (don't wait for sync)
    return ProductResponse(
        message=f"Produk ID {result} berhasil dibuat",
        data=produk_dict
    )
```

**Step 6: Search Service - Index**
```python
# Receive sync request
@router.post("/sync/single")
async def sync_single_product(product: Dict[str, Any]):
    # Remove _id from body (ES metadata)
    doc_body = {k: v for k, v in product.items() if k != "_id"}
    
    # Index to Elasticsearch
    doc_id = product["_id"]
    client.index(
        index="produk",
        id=doc_id,
        body=doc_body
    )
    
    # Refresh index (make searchable)
    client.indices.refresh(index="produk")
```

**Step 7-8: Response & UI Update**
```python
# Core Service returns
{
  "status": "success",
  "message": "Produk ID 1 berhasil dibuat",
  "data": {
    "_id": 1,
    "nama": "Laptop Asus ROG",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB"
  }
}

# Frontend receives and updates UI
```

---

### 2.2 READ Products

#### Flow Diagram
```
┌──────────┐
│  User    │
│  Action: │
│  View    │
│  Products│
└────┬─────┘
     │
     │ 1. Navigate to products page
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Load page        │
└────┬────────────────┘
     │
     │ 2. GET /api/products
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Check MongoDB    │
└────┬────────────────┘
     │
     │ 3. find({})
     ▼
┌─────────────────────┐
│   MongoDB           │
│                     │
│  - Query all        │
│  - Convert _id      │
│  - Return list      │
└────┬────────────────┘
     │
     │ 4. [{_id: 1, ...}, {_id: 2, ...}]
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Wrap response    │
└────┬────────────────┘
     │
     │ 5. 200 OK
     │    {message: "Ditemukan 12 produk", data: [...], total: 12}
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Display products │
│  - Render cards     │
└────┬────────────────┘
     │
     │ 6. User sees product list
     ▼
┌──────────┐
│  User    │
│  Views   │
│  Products│
└──────────┘
```

#### Detailed Steps

**Step 1-2: Frontend → Core Service**
```javascript
// Frontend loads page
onMounted(async () => {
  const response = await axios.get('/api/products')
  products.value = response.data.data
})
```

**Step 3: Core Service → MongoDB**
```python
@router.get("/products")
async def get_all_products():
    products = mongo.cari_semua()
    # Calls MongoDB find({})
```

**Step 4: MongoDB Query**
```python
# mongo_service.py
def cari_semua():
    collection = dapatkan_koleksi()
    data = list(collection.find({}))
    
    # Convert ObjectId to string
    for item in data:
        item["_id"] = str(item["_id"])
    
    return data
```

```javascript
// MongoDB executes
db.products.find({})

// Returns
[
  {_id: 1, nama: "Laptop", ...},
  {_id: 2, nama: "Phone", ...},
  ...
]
```

**Step 5-6: Response & Display**
```python
# Core Service returns
{
  "status": "success",
  "message": "Ditemukan 12 produk",
  "data": [...],
  "total": 12
}

# Frontend displays
```

---

### 2.3 UPDATE Product

#### Flow Diagram
```
┌──────────┐
│  User    │
│  Action: │
│  Update  │
└────┬─────┘
     │
     │ 1. Edit form & submit
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Validate input   │
└────┬────────────────┘
     │
     │ 2. PUT /api/products/1
     │    {nama: "New Name", harga: 2000000}
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Validate schema  │
│  - Check exists     │
└────┬────────────────┘
     │
     │ 3. update_one()
     ▼
┌─────────────────────┐
│   MongoDB           │
│                     │
│  - Update document  │
│  - Return modified  │
└────┬────────────────┘
     │
     │ 4. Success
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Create sync task │
│  - Fetch updated    │
└────┬────────────────┘
     │
     │ 5. (Async) PUT /api/sync/1
     │    {nama: "New Name", harga: 2000000}
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Update document  │
│  - Refresh index    │
└────┬────────────────┘
     │
     │ 6. 200 OK
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Return updated   │
└────┬────────────────┘
     │
     │ 7. 200 OK
     │    {message: "Produk ID 1 berhasil diupdate", data: {...}}
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Show success     │
│  - Update UI        │
└────┬────────────────┘
     │
     │ 8. Display updated product
     ▼
┌──────────┐
│  User    │
│  Sees    │
│  updated │
│  product │
└──────────┘
```

#### Detailed Steps

**Step 1-2: Frontend → Core Service**
```javascript
// User edits product
const updatedData = {
  nama: "Laptop Asus ROG Zephyrus G14 (Updated)",
  harga: 19999000
}

// Send PUT request
const response = await axios.put('/api/products/1', updatedData)
```

**Step 3: Core Service - Validation & Update**
```python
@router.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdateSchema):
    # Check if product exists
    existing = mongo.cari_by_id(product_id)
    if not existing:
        raise HTTPException(404, "Produk tidak ditemukan")
    
    # Get only non-None fields
    data_baru = product.model_dump(exclude_none=True, by_alias=True)
    
    # Update MongoDB
    berhasil = mongo.update_data(product_id, data_baru)
```

**Step 4: MongoDB Update**
```python
# mongo_service.py
def update_data(produk_id, data_baru):
    result = collection.update_one(
        {"_id": produk_id},
        {"$set": data_baru}
    )
    return result.modified_count > 0
```

```javascript
// MongoDB executes
db.products.updateOne(
  {_id: 1},
  {$set: {nama: "New Name", harga: 2000000}}
)
```

**Step 5-6: Sync to Search Service**
```python
    # Sync to Search Service (async)
    asyncio.create_task(
        sinkronisasi_ke_search_service("PUT", f"/sync/{product_id}", data_baru)
    )
    
    # Fetch updated data
    updated = mongo.cari_by_id(product_id)
    
    return ProductResponse(
        message=f"Produk ID {product_id} berhasil diupdate",
        data=updated
    )
```

**Step 7-8: Response & UI Update**
```python
# Response
{
  "status": "success",
  "message": "Produk ID 1 berhasil diupdate",
  "data": {
    "_id": 1,
    "nama": "New Name",
    "harga": 2000000,
    ...
  }
}

# Frontend updates UI
```

---

### 2.4 DELETE Product

#### Flow Diagram
```
┌──────────┐
│  User    │
│  Action: │
│  Delete  │
└────┬─────┘
     │
     │ 1. Click delete button
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Confirm dialog   │
└────┬────────────────┘
     │
     │ 2. DELETE /api/products/1
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Check exists     │
└────┬────────────────┘
     │
     │ 3. delete_one()
     ▼
┌─────────────────────┐
│   MongoDB           │
│                     │
│  - Delete document  │
│  - Return deleted   │
└────┬────────────────┘
     │
     │ 4. Success
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Create sync task │
└────┬────────────────┘
     │
     │ 5. (Async) DELETE /api/sync/1
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Delete document  │
│  - Refresh index    │
└────┬────────────────┘
     │
     │ 6. 200 OK
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Return success   │
└────┬────────────────┘
     │
     │ 7. 200 OK
     │    {message: "Produk ID 1 berhasil dihapus", data: null}
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Remove from list │
│  - Show success     │
└────┬────────────────┘
     │
     │ 8. Product removed from UI
     ▼
┌──────────┐
│  User    │
│  Sees    │
│  product │
│  removed │
└──────────┘
```

#### Detailed Steps

**Step 1-2: Frontend → Core Service**
```javascript
// User clicks delete
const confirmed = confirm("Apakah Anda yakin ingin menghapus produk ini?")
if (confirmed) {
  const response = await axios.delete('/api/products/1')
  // Remove from list
  products.value = products.value.filter(p => p._id !== 1)
}
```

**Step 3: Core Service - Validation & Delete**
```python
@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    # Check if product exists
    existing = mongo.cari_by_id(product_id)
    if not existing:
        raise HTTPException(404, "Produk tidak ditemukan")
    
    # Delete from MongoDB
    berhasil = mongo.delete_data(product_id)
```

**Step 4: MongoDB Delete**
```python
# mongo_service.py
def delete_data(produk_id):
    result = collection.delete_one({"_id": produk_id})
    return result.deleted_count > 0
```

```javascript
// MongoDB executes
db.products.deleteOne({_id: 1})

// Returns: {acknowledged: true, deletedCount: 1}
```

**Step 5-6: Sync to Search Service**
```python
    # Sync to Search Service (async)
    asyncio.create_task(
        sinkronisasi_ke_search_service("DELETE", f"/sync/{product_id}")
    )
    
    return ProductResponse(
        message=f"Produk ID {product_id} berhasil dihapus",
        data=None
    )
```

**Step 7-8: Response & UI Update**
```python
# Response
{
  "status": "success",
  "message": "Produk ID 1 berhasil dihapus",
  "data": null
}

# Frontend removes product from list
```

---

## 3. Search Flow

### 3.1 Full-Text Search

#### Flow Diagram
```
┌──────────┐
│  User    │
│  Action: │
│  Search  │
└────┬─────┘
     │
     │ 1. Type "laptop gaming" in search box
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Debounce input   │
│  - Send request     │
└────┬────────────────┘
     │
     │ 2. GET /api/search?q=laptop gaming
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Receive query    │
└────┬────────────────┘
     │
     │ 3. Analyze query
     │    "laptop gaming" → ["laptop", "gaming"]
     ▼
┌─────────────────────┐
│   Elasticsearch     │
│                     │
│  - Lookup inverted  │
│    index            │
│  - "laptop" → [1,5] │
│  - "gaming" → [5,12] │
└────┬────────────────┘
     │
     │ 4. Calculate scores
     │    Doc 1: 0.85
     │    Doc 5: 2.45
     │    Doc 12: 1.89
     ▼
┌─────────────────────┐
│   Elasticsearch     │
│                     │
│  - Sort by score    │
│  - Return top N     │
└────┬────────────────┘
     │
     │ 5. [{_source: {...}, _score: 2.45}, ...]
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Extract _source  │
│  - Format response  │
└────┬────────────────┘
     │
     │ 6. 200 OK
     │    {message: "Ditemukan 3 hasil", data: [...], total: 3}
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Display results  │
│  - Highlight match  │
└────┬────────────────┘
     │
     │ 7. User sees search results
     ▼
┌──────────┐
│  User    │
│  Views   │
│  results │
└──────────┘
```

#### Detailed Steps

**Step 1-2: Frontend → Search Service**
```javascript
// User types in search box
const query = 'laptop gaming'

// Debounce (wait 300ms after typing stops)
const response = await axios.get(`http://localhost:8002/api/search?q=${query}`)
```

**Step 3: Search Service - Query Analysis**
```python
@router.get("/search")
async def search_products(q: str):
    # Receive query
    # q = "laptop gaming"
    
    # Call Elasticsearch
    hasil = es.cari_match(q)
```

**Step 4: Elasticsearch - Search Execution**
```python
# elastic_service.py
def cari_match(keyword: str):
    query = {
        "query": {
            "multi_match": {
                "query": keyword,  # "laptop gaming"
                "fields": ["nama", "kategori", "spesifikasi"],
                "type": "best_fields"
            }
        }
    }
    
    response = client.search(index="produk", body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]
```

**Elasticsearch Process:**
```
1. Query Analysis
   "laptop gaming" → ["laptop", "gaming"]

2. Inverted Index Lookup
   "laptop" → [1, 5, 12, 23, 45]
   "gaming" → [5, 12, 23]

3. Merge Results (AND)
   Intersection: [5, 12, 23]

4. Calculate Scores
   Doc 5: TF(laptop)=2, TF(gaming)=1 → Score: 2.45
   Doc 12: TF(laptop)=1, TF(gaming)=1 → Score: 1.89
   Doc 23: TF(laptop)=1, TF(gaming)=1 → Score: 1.23

5. Sort by Score
   [Doc 5 (2.45), Doc 12 (1.89), Doc 23 (1.23)]

6. Return Top N
   Top 10 results
```

**Step 5-7: Response & Display**
```python
# Search Service returns
{
  "status": "success",
  "message": "Ditemukan 3 hasil untuk 'laptop gaming'",
  "data": [
    {
      "nama": "Laptop Gaming Asus ROG",
      "kategori": "Laptop",
      "harga": 18999000,
      ...
    },
    ...
  ],
  "total": 3,
  "keyword": "laptop gaming"
}

# Frontend displays results
```

---

## 4. Synchronization Flow

### 4.1 Real-time Sync (CRUD → Elasticsearch)

#### Flow Diagram
```
┌──────────────────────────────────────────────────────────┐
│  Core Service                                            │
│                                                          │
│  Operation: CREATE/UPDATE/DELETE                         │
│       │                                                  │
│       │ 1. Execute MongoDB operation                     │
│       ▼                                                  │
│  ┌──────────────┐                                        │
│  │   MongoDB    │                                        │
│  │  (Success)   │                                        │
│  └──────┬───────┘                                        │
│         │                                                │
│         │ 2. Create async sync task                      │
│         ▼                                                │
│  ┌──────────────────────┐                                │
│  │ asyncio.create_task │                                │
│  │ (fire-and-forget)   │                                │
│  └──────┬──────────────┘                                │
│         │                                                │
│         │ 3. Return response to client                   │
│         ▼                                                │
│  ┌──────────────────────┐                                │
│  │ HTTP 200/201 OK     │                                │
│  │ (Client happy)      │                                │
│  └──────────────────────┘                                │
│                                                          │
│  Background Task:                                        │
│       │                                                  │
│       │ 4. HTTP POST/PUT/DELETE                           │
│       ▼                                                  │
│  ┌──────────────────────┐                                │
│  │ Search Service      │                                │
│  │ (Receive sync)      │                                │
│  └──────┬──────────────┘                                │
│         │                                                │
│         │ 5. Execute ES operation                         │
│         ▼                                                │
│  ┌──────────────────────┐                                │
│  │ Elasticsearch       │                                │
│  │ (Index/Update/Delete)│                               │
│  └──────────────────────┘                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### Detailed Steps

**Step 1-3: Core Service (Synchronous)**
```python
# 1. Execute MongoDB operation
produk_dict = product.model_dump(by_alias=True)
result = mongo.insert_satu(produk_dict)

# 2. Create async sync task (fire-and-forget)
asyncio.create_task(
    sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
)

# 3. Immediately return response (don't wait for sync)
return ProductResponse(
    message=f"Produk ID {result} berhasil dibuat",
    data=produk_dict
)
```

**Step 4-5: Background Sync (Asynchronous)**
```python
# Background task runs independently
async def sinkronisasi_ke_search_service(method, endpoint, data):
    url = f"http://search-service:8002/api{endpoint}"
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        if method == "POST":
            await client.post(url, json=data)
        elif method == "PUT":
            await client.put(url, json=data)
        elif method == "DELETE":
            await client.delete(url)
```

**Step 6: Search Service - Elasticsearch Operation**
```python
# Search Service receives sync request
@router.post("/sync/single")
async def sync_single_product(product: Dict[str, Any]):
    # Index to Elasticsearch
    doc_id = product["_id"]
    doc_body = {k: v for k, v in product.items() if k != "_id"}
    
    client.index(
        index="produk",
        id=doc_id,
        body=doc_body
    )
    
    # Refresh index
    client.indices.refresh(index="produk")
```

---

### 4.2 Bulk Sync (Seed Data)

#### Flow Diagram
```
┌──────────┐
│  Admin   │
│  Action: │
│  Seed    │
└────┬─────┘
     │
     │ 1. POST /api/products/seed
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Load JSON file   │
└────┬────────────────┘
     │
     │ 2. insert_many()
     ▼
┌─────────────────────┐
│   MongoDB           │
│                     │
│  - Delete old data  │
│  - Insert 12 docs   │
└────┬────────────────┘
     │
     │ 3. Success (12 inserted)
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Sync all data    │
└────┬────────────────┘
     │
     │ 4. POST /api/sync
     │    {products: [{...}, {...}, ...]}
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Delete index     │
│  - Recreate index   │
│  - Index all docs   │
└────┬────────────────┘
     │
     │ 5. 201 Created
     ▼
┌─────────────────────┐
│   Core Service      │
│                     │
│  - Return success   │
└────┬────────────────┘
     │
     │ 6. 201 Created
     │    {message: "Berhasil seed 12 produk", ...}
     ▼
┌──────────┐
│  Admin   │
│  Sees    │
│  success │
└──────────┘
```

#### Detailed Steps

**Step 1-2: Core Service - Load & Insert**
```python
@router.post("/products/seed")
async def seed_products():
    # Load dataset from JSON
    data = mongo.muat_dataset()
    # Returns: [{_id: 1, ...}, {_id: 2, ...}, ...]
    
    # Insert to MongoDB (bulk)
    jumlah = mongo.insert_banyak(data)
    # MongoDB: delete_many({}) then insert_many(data)
```

**Step 3-4: Core Service - Bulk Sync**
```python
    # Sync all data to Search Service
    await sinkronisasi_ke_search_service("POST", "/sync", {"products": data})
```

**Step 5: Search Service - Bulk Index**
```python
@router.post("/sync")
async def sync_products(request: SyncRequest):
    # Index banyak (bulk)
    jumlah = es.index_banyak(request.products)
```

```python
# elastic_service.py
def index_banyak(data_list):
    # Delete old index
    if client.indices.exists(index=ELASTIC_INDEX_NAME):
        client.indices.delete(index=ELASTIC_INDEX_NAME)
    
    # Create new index
    buat_index()
    
    # Index all documents
    for data in data_list:
        doc_id = data["_id"]
        doc_body = {k: v for k, v in data.items() if k != "_id"}
        client.index(index=ELASTIC_INDEX_NAME, id=doc_id, body=doc_body)
    
    # Refresh index
    client.indices.refresh(index=ELASTIC_INDEX_NAME)
```

**Step 6: Response**
```python
# Response
{
  "status": "success",
  "message": "Berhasil seed 12 produk ke MongoDB dan Elasticsearch",
  "data": [...],
  "total": 12
}
```

---

## 5. Error Handling Flow

### 5.1 Validation Error

```
User Input: {_id: "invalid", nama: ""}
    ↓
Frontend: HTML5 validation
    ↓
Core Service: Pydantic validation
    ↓
Error: {"detail": "Validation error"}
    ↓
Frontend: Show error message
    ↓
User: Correct input
```

### 5.2 Not Found Error

```
Request: GET /api/products/999
    ↓
Core Service: Check MongoDB
    ↓
MongoDB: No document found
    ↓
Error: {"detail": "Produk dengan ID 999 tidak ditemukan"}
    ↓
Frontend: Show "Not Found" message
    ↓
User: See error message
```

### 5.3 Database Connection Error

```
Request: POST /api/products
    ↓
Core Service: Check MongoDB connection
    ↓
Error: MongoDB not available
    ↓
Error: {"detail": "MongoDB tidak tersedia"}
    ↓
Frontend: Show "Service Unavailable"
    ↓
User: Try again later
```

### 5.4 Sync Error (Non-blocking)

```
Core Service: Product created in MongoDB
    ↓
Core Service: Try sync to Search Service
    ↓
Search Service: Unavailable (timeout)
    ↓
Core Service: Log warning (don't fail)
    ↓
Core Service: Return success to user
    ↓
User: Product created (sync will retry later)
    ↓
Search Service: Back online
    ↓
Manual: Re-seed data or sync manually
```

---

## 6. Data Consistency Flow

### 6.1 Strong Consistency (MongoDB)
```
Write Operation
    ↓
MongoDB (Primary)
    ↓
Acknowledge (immediate)
    ↓
Read Operation
    ↓
MongoDB (Primary/Secondary)
    ↓
Return latest data (strong consistency)
```

### 6.2 Eventual Consistency (Elasticsearch)
```
Write Operation
    ↓
Elasticsearch (Index)
    ↓
Refresh (1 second default)
    ↓
Searchable (near real-time)
    ↓
User search
    ↓
May not see latest data immediately (eventual consistency)
```

### 6.3 Sync Strategy
```
MongoDB (Source of Truth)
    ↓
Real-time sync (async)
    ↓
Elasticsearch (Search Index)
    ↓
Eventual consistency (acceptable for search)
```

---

## 7. Performance Flow

### 7.1 Response Time Breakdown

#### CRUD Operation
```
Client Request
    ↓
Network (1-10ms)
    ↓
Frontend Processing (5-20ms)
    ↓
Network (1-10ms)
    ↓
Core Service Validation (5-10ms)
    ↓
MongoDB Query (10-50ms)
    ↓
Network (1-10ms)
    ↓
Core Service Response (5-10ms)
    ↓
Network (1-10ms)
    ↓
Frontend Rendering (10-50ms)
    ↓
Total: 40-160ms
```

#### Search Operation
```
Client Request
    ↓
Network (1-10ms)
    ↓
Frontend Processing (5-20ms)
    ↓
Network (1-10ms)
    ↓
Search Service (5-10ms)
    ↓
Elasticsearch Query (10-50ms)
    ↓
Network (1-10ms)
    ↓
Search Service Response (5-10ms)
    ↓
Network (1-10ms)
    ↓
Frontend Rendering (10-50ms)
    ↓
Total: 40-160ms
```

### 7.2 Optimization Strategies

#### Caching (Future)
```
Request
    ↓
Check Cache (Redis)
    ↓
Hit: Return cached data (1-5ms)
Miss: Fetch from database
    ↓
Store in cache
    ↓
Return data
```

#### Connection Pooling
```
Application Start
    ↓
Create Connection Pool (10-20 connections)
    ↓
Request
    ↓
Get connection from pool
    ↓
Execute query
    ↓
Return connection to pool
    ↓
Response
```

---

## 8. Docker Flow

### 8.1 Container Lifecycle

```
docker-compose up -d
    ↓
Create Network
    ↓
Create Volumes
    ↓
Pull Images (if needed)
    ↓
Build Images (if needed)
    ↓
Create Containers
    ↓
Start Containers
    ↓
Health Checks
    ↓
All Services Running
```

### 8.2 Data Persistence

```
Container Start
    ↓
Mount Volume
    ↓
Read Data from Volume
    ↓
Application Runs
    ↓
Data Written to Volume
    ↓
Container Stop
    ↓
Data Persists in Volume
    ↓
Container Start (again)
    ↓
Read Data from Volume
    ↓
Application Runs (data still there)
```

### 8.3 Service Communication

```
Core Service Container
    │
    │ "I need to talk to Search Service"
    ▼
Docker DNS
    │
    │ "search-service" → 172.20.0.3
    ▼
Network Route
    │
    │ Route to 172.20.0.3:8002
    ▼
Search Service Container
    │
    │ "I received the request"
    ▼
Response
```

---

## 9. Complete System Flow Example

### Scenario: User Creates Product and Searches It

```
TIME    ACTION                           COMPONENT              STATUS
──────────────────────────────────────────────────────────────────────
0ms     User clicks "Create Product"     Frontend               Ready
10ms    Form validation                  Frontend               Valid
20ms    POST /api/products               Frontend → Core        Sending
30ms    Pydantic validation              Core Service           Valid
40ms    Check duplicate                  Core Service → Mongo   Query
50ms    Insert to MongoDB                MongoDB                Success
60ms    Return to Core Service           MongoDB → Core         Success
70ms    Create sync task                 Core Service           Async
80ms    Return 201 Created               Core Service → Frontend Success
90ms    Display success message          Frontend               Updated
100ms   User sees "Product created"      Frontend               Complete
        ─────────────────────────────────────────────────────────────
        (Meanwhile, async sync happens)
150ms   POST /api/sync/single            Core → Search          Sending
160ms   Index to Elasticsearch           Search Service → ES    Indexing
170ms   Refresh index                    Elasticsearch          Complete
180ms   Return 201 Created               Search → Core          Success
        ─────────────────────────────────────────────────────────────
        (User searches for the product)
200ms   User types "laptop"              Frontend               Input
250ms   Debounce (300ms wait)            Frontend               Waiting
550ms   GET /api/search?q=laptop         Frontend → Search      Sending
560ms   Query analysis                   Search Service         Analyzing
570ms   Inverted index lookup            Elasticsearch          Fast lookup
580ms   Calculate scores                 Elasticsearch          Scoring
590ms   Sort results                     Elasticsearch          Sorting
600ms   Return results                   ES → Search → Frontend Success
610ms   Display results                  Frontend               Updated
620ms   User sees search results         Frontend               Complete
```

---

## Summary

### Key Flows
1. **Startup**: Docker Compose orchestrates all services
2. **CRUD**: Frontend → Core Service → MongoDB + Async Sync → Elasticsearch
3. **Search**: Frontend → Search Service → Elasticsearch → Results
4. **Sync**: Real-time async sync after each CRUD operation
5. **Error Handling**: Graceful degradation, non-blocking sync errors
6. **Performance**: Sub-200ms response times for all operations
7. **Docker**: Containerization ensures consistency and portability

### Important Patterns
- **Fire-and-Forget**: Sync happens in background, user doesn't wait
- **Eventual Consistency**: Elasticsearch eventually consistent (acceptable)
- **Strong Consistency**: MongoDB strongly consistent (source of truth)
- **Separation of Concerns**: Each service has clear responsibility
- **Async Communication**: Non-blocking operations for better UX