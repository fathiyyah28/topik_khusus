# PERBANDINGAN MONGODB DAN ELASTICSEARCH

## Overview
Bagian ini membandingkan MongoDB dan Elasticsearch secara detail untuk memahami perbedaan kedua database ini dan mengapa keduanya digunakan bersama dalam project ini.

---

## 1. Konsep Dasar

### 1.1 MongoDB (Document Database)

#### Definisi
MongoDB adalah NoSQL document database yang dirancang untuk penyimpanan dan pengambilan data (CRUD operations) dengan schema yang fleksibel.

#### Primary Purpose
- **CRUD Operations**: Create, Read, Update, Delete
- **Primary Data Storage**: Menyimpan data utama aplikasi
- **Transactional Data**: Data yang memerlukan konsistensi kuat

#### Konsep Kunci
```
Database → Collection → Document → Field

Example:
Database: uas_db
  Collection: products
    Document: {
      _id: 1,
      nama: "Laptop",
      harga: 5000000,
      stok: 10
    }
```

#### Strengths
✅ Fast CRUD operations  
✅ Flexible schema  
✅ Horizontal scalability  
✅ JSON-like format  
✅ High write throughput  

### 1.2 Elasticsearch (Search Engine)

#### Definisi
Elasticsearch adalah distributed search dan analytics engine yang dirancang untuk full-text search, log analytics, dan application monitoring.

#### Primary Purpose
- **Full-Text Search**: Pencarian teks yang advanced
- **Search Index**: Index untuk fast lookup
- **Analytics**: Data analysis dan aggregation

#### Konsep Kunci
```
Cluster → Index → Document → Field

Example:
Cluster: uas-cluster
  Index: produk
    Document: {
      _id: 1,
      nama: "Laptop",
      harga: 5000000
    }
```

#### Strengths
✅ Full-text search  
✅ Relevance scoring (BM25)  
✅ Fuzzy matching  
✅ Inverted index (fast lookup)  
✅ Horizontal scalability  

---

## 2. Perbandingan Detail

### 2.1 Primary Purpose

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Main Purpose** | CRUD operations | Full-text search |
| **Data Storage** | Primary storage | Search index (secondary) |
| **Consistency** | Strong consistency | Eventual consistency |
| **Use Case** | Transactional data | Search & analytics |

#### MongoDB - Source of Truth
```python
# MongoDB menyimpan data asli
# Semua operasi CRUD di sini

# CREATE
db.products.insertOne({
  _id: 1,
  nama: "Laptop",
  harga: 5000000
})

# READ
db.products.find({harga: {$gt: 1000000}})

# UPDATE
db.products.updateOne({_id: 1}, {$set: {harga: 6000000}})

# DELETE
db.products.deleteOne({_id: 1})
```

#### Elasticsearch - Search Index
```python
# Elasticsearch menyimpan copy untuk search
# Hanya untuk pencarian, bukan sumber data

# Index document
client.index(
  index="produk",
  id=1,
  body={
    "nama": "Laptop",
    "harga": 5000000
  }
)

# Search
client.search(
  index="produk",
  body={
    "query": {
      "match": {"nama": "laptop"}
    }
  }
)
```

### 2.2 Data Model

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Structure** | Document (JSON-like) | Document (JSON) |
| **Schema** | Flexible | Mapping (schema definition) |
| **Nested Data** | Native support | Supported |
| **Arrays** | Native support | Supported |

#### MongoDB Document
```javascript
{
  "_id": 1,
  "nama": "Laptop Asus ROG",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": {
    "processor": "AMD Ryzen 9",
    "ram": "16GB",
    "storage": "SSD 512GB"
  },
  "tags": ["gaming", "high-performance"],
  "created_at": ISODate("2024-01-15T10:30:00Z")
}
```

#### Elasticsearch Document
```json
{
  "_id": "1",
  "_source": {
    "nama": "Laptop Asus ROG",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB"
  },
  "_score": 2.45
}
```

**Key Difference**: 
- MongoDB: `_id` is part of document
- Elasticsearch: `_id` is metadata, `_source` contains actual data

### 2.3 Query Capabilities

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **CRUD** | Excellent | Limited (index/update/delete) |
| **Search** | Basic (regex) | Excellent (full-text) |
| **Aggregation** | Excellent | Excellent |
| **Complex Queries** | Good | Excellent |
| **Joins** | Limited | No joins |

#### MongoDB Queries
```javascript
// CRUD Operations
db.products.insertOne({nama: "Laptop", harga: 5000000})
db.products.find({harga: {$gt: 1000000}})
db.products.updateOne({_id: 1}, {$set: {harga: 6000000}})
db.products.deleteOne({_id: 1})

// Aggregation
db.products.aggregate([
  {$match: {kategori: "Laptop"}},
  {$group: {_id: "$kategori", total: {$sum: "$stok"}}}
])

// Regex Search (SLOW!)
db.products.find({
  nama: {$regex: "laptop", $options: "i"}
})
```

#### Elasticsearch Queries
```python
# Search Operations
client.search(
  index="produk",
  body={
    "query": {
      "multi_match": {
        "query": "laptop gaming",
        "fields": ["nama", "kategori", "spesifikasi"]
      }
    }
  }
)

# Fuzzy Search
client.search(
  index="produk",
  body={
    "query": {
      "fuzzy": {
        "nama": {
          "value": "lapto",
          "fuzziness": "AUTO"
        }
      }
    }
  }
)

# Aggregation
client.search(
  index="produk",
  body={
    "aggs": {
      "kategori_count": {
        "terms": {"field": "kategori"}
      }
    }
  }
)
```

**Key Difference**:
- MongoDB: Best untuk CRUD
- Elasticsearch: Best untuk search

### 2.4 Indexing

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Index Type** | B-tree, Hash, Text | Inverted Index |
| **Purpose** | Fast data retrieval | Fast text search |
| **Structure** | Key → Document | Token → Document IDs |
| **Performance** | O(log n) | O(1) |

#### MongoDB Index
```javascript
// B-tree index
db.products.createIndex({nama: 1})

// Query uses index
db.products.find({nama: "Laptop"})
// Fast: O(log n)

// Text index (basic)
db.products.createIndex({nama: "text", kategori: "text"})
db.products.find({$text: {$search: "laptop"}})
// Still slower than Elasticsearch
```

#### Elasticsearch Inverted Index
```python
# Inverted index structure
{
  "laptop": [1, 5, 12, 23, 45],
  "gaming": [5, 12, 23],
  "asus": [1, 12]
}

# Search "laptop gaming"
# Direct lookup: O(1)
# Find intersection: [5, 12, 23]
# Super fast!
```

**Key Difference**:
- MongoDB: B-tree indexes (good untuk exact matches)
- Elasticsearch: Inverted indexes (excellent untuk full-text search)

### 2.5 Performance

| Operation | MongoDB | Elasticsearch |
|-----------|---------|---------------|
| **Insert** | ~10ms | ~10ms |
| **Update** | ~10ms | ~10ms |
| **Delete** | ~10ms | ~10ms |
| **Find by ID** | ~5ms | ~5ms |
| **Full-text Search** | ~500ms (slow) | ~10ms (fast) |
| **Regex Search** | ~500ms | N/A |

#### Performance Comparison: Search

**MongoDB Regex Search:**
```
Dataset: 100,000 products
Query: "laptop gaming"
Time: ~5,000ms (5 seconds!)
Method: Full collection scan
CPU: High
```

**Elasticsearch Search:**
```
Dataset: 100,000 products
Query: "laptop gaming"
Time: ~20ms
Method: Inverted index lookup
CPU: Low
```

**Speed Difference**: 250x faster!

### 2.6 Consistency Model

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Consistency** | Strong (immediate) | Eventual (near real-time) |
| **Write Acknowledge** | Immediate | After refresh |
| **Read Your Writes** | Yes | Usually (1 second delay) |
| **Use Case** | Source of truth | Search index |

#### MongoDB - Strong Consistency
```python
# Write
collection.insert_one({"_id": 1, "nama": "Laptop"})
# Immediately available

# Read
doc = collection.find_one({"_id": 1})
# Returns latest data immediately
```

#### Elasticsearch - Eventual Consistency
```python
# Index
client.index(index="produk", id=1, body={"nama": "Laptop"})
# Not immediately searchable!

# Wait for refresh (default: 1 second)
import time
time.sleep(1)

# Now searchable
results = client.search(index="produk", body={"query": {"match": {"nama": "Laptop"}}})
```

**Key Difference**:
- MongoDB: Write → Immediately readable
- Elasticsearch: Write → Searchable after ~1 second

### 2.7 Scalability

| Aspek | MongoDB | Elasticsearch |
|-------|---------|---------------|
| **Scaling** | Horizontal + Vertical | Horizontal + Vertical |
| **Sharding** | Native | Native |
| **Replication** | Replica sets | Cluster nodes |
| **Max Size** | Unlimited | Unlimited |

#### MongoDB Scaling
```javascript
// Sharding (horizontal scaling)
// Automatic data distribution

// Replica set (high availability)
rs.initiate({
  _id: "rs0",
  members: [
    {_id: 0, host: "mongodb0:27017"},
    {_id: 1, host: "mongodb1:27017"},
    {_id: 2, host: "mongodb2:27017"}
  ]
})
```

#### Elasticsearch Scaling
```json
// Cluster with multiple nodes
{
  "cluster": {
    "name": "uas-cluster",
    "nodes": [
      {"master": true, "data": true},
      {"master": false, "data": true},
      {"master": false, "data": true}
    ]
  }
}

// Automatic sharding
// Index "produk" split into 3 shards
// Each shard replicated to 2 nodes
```

**Similarity**: Both support horizontal scaling

---

## 3. Comparison Table

| Feature | MongoDB | Elasticsearch |
|---------|---------|---------------|
| **Type** | Document Database | Search Engine |
| **Primary Use** | CRUD operations | Full-text search |
| **Schema** | Flexible | Mapping required |
| **Query Language** | MongoDB Query | Query DSL |
| **Index Type** | B-tree | Inverted Index |
| **Search Speed** | Slow (O(n)) | Fast (O(1)) |
| **CRUD Speed** | Very Fast | Limited |
| **Consistency** | Strong | Eventual |
| **Transactions** | Full ACID | No transactions |
| **Scaling** | Horizontal | Horizontal |
| **Best For** | Data storage | Search & analytics |
| **Use in Project** | Primary DB | Search index |

---

## 4. Kapan Menggunakan MongoDB?

### ✅ Gunakan MongoDB Untuk:

1. **Primary Data Storage**
   - Menyimpan data utama aplikasi
   - Source of truth
   - CRUD operations

2. **Flexible Schema**
   - Data structure berubah-ubah
   - Rapid development
   - Agile iteration

3. **High Write Throughput**
   - IoT data ingestion
   - Real-time data collection
   - Logging

4. **Complex Data Models**
   - Nested documents
   - Arrays
   - Hierarchical data

5. **Transactions**
   - ACID compliance needed
   - Multi-document transactions
   - Data consistency critical

### Contoh Use Case MongoDB:
- User profiles
- Product catalogs
- Content management
- IoT data
- Real-time applications
- Mobile apps

---

## 5. Kapan Menggunakan Elasticsearch?

### ✅ Gunakan Elasticsearch Untuk:

1. **Full-Text Search**
   - Pencarian teks yang advanced
   - Relevance scoring
   - Fuzzy matching

2. **Search-Heavy Applications**
   - E-commerce search
   - Content search
   - Log search

3. **Analytics**
   - Data aggregation
   - Metrics calculation
   - Business intelligence

4. **Large-Scale Search**
   - Millions of documents
   - High search volume
   - Complex queries

5. **Real-Time Search**
   - Near real-time indexing
   - Instant search results
   - Auto-complete

### Contoh Use Case Elasticsearch:
- E-commerce product search
- Log analytics (ELK stack)
- Application monitoring
- Content search
- Autocomplete & suggestions
- Business analytics

---

## 6. Mengapa Project Ini Menggunakan Keduanya?

### 6.1 Complementary Roles

```
┌─────────────────────────────────────────┐
│         SYSTEM ARCHITECTURE             │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   MongoDB    │    │ Elasticsearch│  │
│  │              │    │              │  │
│  │  - CRUD      │    │  - Search    │  │
│  │  - Storage   │    │  - Index     │  │
│  │  - Source    │    │  - Fast      │  │
│  │    of Truth  │    │    Lookup    │  │
│  └──────┬───────┘    └──────┬───────┘  │
│         │                   │           │
│         │   Sync (async)    │           │
│         │<──────────────────>│           │
│         │                   │           │
└─────────┼───────────────────┼───────────┘
          │                   │
          ▼                   ▼
   ┌──────────────┐   ┌──────────────┐
   │ Core Service │   │Search Service│
   │  (CRUD)      │   │  (Search)    │
   └──────────────┘   └──────────────┘
```

### 6.2 Why Both?

#### MongoDB untuk CRUD
```python
# Fast CRUD operations
# Strong consistency
# Flexible schema
# Source of truth

# Example: Create product
product = {
  "_id": 1,
  "nama": "Laptop",
  "harga": 5000000,
  "stok": 10
}
db.products.insert_one(product)
# Immediately available for reads
```

#### Elasticsearch untuk Search
```python
# Fast full-text search
# Relevance scoring
# Fuzzy matching
# Search index

# Example: Search product
results = es.search(
  index="produk",
  body={
    "query": {
      "multi_match": {
        "query": "laptop gaming",
        "fields": ["nama", "kategori"]
      }
    }
  }
)
# Results in ~10ms with relevance scoring
```

### 6.3 Synchronization Strategy

```python
# Core Service performs CRUD on MongoDB
# Then syncs to Elasticsearch (async)

# 1. Create in MongoDB
db.products.insert_one(product)

# 2. Sync to Elasticsearch (fire-and-forget)
asyncio.create_task(
  sync_to_search_service("POST", "/sync/single", product)
)

# 3. Return success to user
# User doesn't wait for sync

# Background: Elasticsearch indexing happens
# Delay: ~1 second (refresh interval)
# Result: Eventually consistent (acceptable for search)
```

### 6.4 Benefits of This Approach

✅ **Best of Both Worlds**
   - MongoDB: Fast CRUD
   - Elasticsearch: Fast search

✅ **Separation of Concerns**
   - MongoDB: Data storage
   - Elasticsearch: Search optimization

✅ **Scalability**
   - Scale MongoDB untuk writes
   - Scale Elasticsearch untuk searches

✅ **Performance**
   - CRUD: ~10-50ms (MongoDB)
   - Search: ~10-50ms (Elasticsearch)
   - Best performance for each operation

✅ **Flexibility**
   - MongoDB schema flexible
   - Elasticsearch mapping optimized for search

---

## 7. Data Flow: MongoDB → Elasticsearch

### 7.1 Sync Process

```
MongoDB (Source of Truth)
    ↓
Core Service detects change
    ↓
Create async sync task
    ↓
HTTP POST to Search Service
    ↓
Search Service receives data
    ↓
Index to Elasticsearch
    ↓
Refresh index
    ↓
Data searchable
```

### 7.2 Sync Implementation

#### Core Service
```python
# After CRUD operation
async def create_product(product):
    # 1. Insert to MongoDB
    db.products.insert_one(product)
    
    # 2. Sync to Elasticsearch (async)
    asyncio.create_task(
        sync_to_search_service("POST", "/sync/single", product)
    )
    
    # 3. Return immediately
    return {"status": "success"}
```

#### Search Service
```python
# Receive sync
@router.post("/sync/single")
async def sync_single_product(product: dict):
    # Remove _id from body (ES metadata)
    doc_body = {k: v for k, v in product.items() if k != "_id"}
    
    # Index to Elasticsearch
    client.index(
        index="produk",
        id=product["_id"],
        body=doc_body
    )
    
    # Refresh index
    client.indices.refresh(index="produk")
    
    return {"status": "success"}
```

### 7.3 Consistency Guarantees

```
MongoDB: Strong Consistency
  - Write acknowledged immediately
  - Read returns latest data
  - ACID compliant

Elasticsearch: Eventual Consistency
  - Write indexed in ~1 second
  - Search may lag 1 second behind
  - Acceptable for search use case

Overall System: Eventually Consistent
  - MongoDB: Always consistent
  - Elasticsearch: Eventually consistent
  - User sees: Near real-time sync
```

---

## 8. Performance Comparison

### 8.1 CRUD Operations

| Operation | MongoDB | Elasticsearch |
|-----------|---------|---------------|
| **Create** | ~10ms | ~10ms |
| **Read by ID** | ~5ms | ~5ms |
| **Update** | ~10ms | ~10ms |
| **Delete** | ~10ms | ~10ms |
| **Complex Query** | ~50ms | N/A |

**Winner**: MongoDB (better untuk CRUD)

### 8.2 Search Operations

| Operation | MongoDB (Regex) | Elasticsearch |
|-----------|-----------------|---------------|
| **Simple Search** | ~500ms | ~10ms |
| **Full-Text Search** | ~5,000ms | ~20ms |
| **Fuzzy Search** | Not supported | ~15ms |
| **Multi-Field Search** | ~1,000ms | ~20ms |
| **Relevance Scoring** | Not supported | Yes (BM25) |

**Winner**: Elasticsearch (50-500x faster!)

### 8.3 Aggregation

| Operation | MongoDB | Elasticsearch |
|-----------|---------|---------------|
| **Simple Aggregation** | ~30ms | ~25ms |
| **Complex Aggregation** | ~100ms | ~50ms |
| **Group By** | ~50ms | ~30ms |
| **Pipeline** | Excellent | Excellent |

**Winner**: Tie (both excellent)

---

## 9. Cost Comparison

### 9.1 Infrastructure

#### MongoDB Only (No Search)
```
MongoDB:
- 2 CPU cores
- 4GB RAM
- 100GB storage
- $57/month

Search: Using MongoDB regex (slow)
- No additional cost
- Poor performance
```

#### Elasticsearch Only (No CRUD)
```
Elasticsearch:
- 2 CPU cores
- 4GB RAM
- 100GB storage
- $57/month

CRUD: Using Elasticsearch (not ideal)
- Possible but not recommended
- No transactions
- Eventual consistency
```

#### Both MongoDB + Elasticsearch (This Project)
```
MongoDB:
- 2 CPU cores
- 4GB RAM
- $57/month

Elasticsearch:
- 2 CPU cores
- 4GB RAM
- $57/month

Total: $114/month

Benefit:
- Best performance for both CRUD and search
- Best user experience
- Scalable
```

**Conclusion**: Cost is worth it for performance

### 9.2 Operational Cost

| Aspect | MongoDB Only | MongoDB + ES |
|--------|--------------|--------------|
| **Development Time** | Fast | Moderate |
| **Maintenance** | Simple | Moderate |
| **Performance** | Poor search | Excellent |
| **User Experience** | Poor | Excellent |
| **Scalability** | Limited | Excellent |

---

## 10. Code Comparison

### 10.1 Insert Data

#### MongoDB
```python
# Insert product
product = {
  "_id": 1,
  "nama": "Laptop Asus",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15
}

db.products.insert_one(product)
# Time: ~10ms
# Immediately available
```

#### Elasticsearch
```python
# Index product
client.index(
  index="produk",
  id=1,
  body={
    "nama": "Laptop Asus",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15
  }
)
# Time: ~10ms
# Searchable after ~1 second
```

### 10.2 Search Data

#### MongoDB (Regex - Slow)
```python
# Search using regex
import re
pattern = re.compile("laptop", re.IGNORECASE)

results = db.products.find({
  "$or": [
    {"nama": {"$regex": pattern}},
    {"kategori": {"$regex": pattern}}
  ]
})

# Time: ~5,000ms for 100,000 docs
# No relevance scoring
# No fuzzy matching
```

#### Elasticsearch (Fast)
```python
# Search using full-text
results = client.search(
  index="produk",
  body={
    "query": {
      "multi_match": {
        "query": "laptop",
        "fields": ["nama", "kategori"]
      }
    }
  }
)

# Time: ~20ms for 100,000 docs
# Relevance scoring included
# Fuzzy matching supported
```

**Speed Difference**: 250x faster!

---

## 11. When to Use Which?

### 11.1 Use MongoDB When:

✅ **Primary Data Storage**
   - Menyimpan data utama
   - Source of truth
   - CRUD operations

✅ **Strong Consistency Required**
   - Data must be immediately consistent
   - ACID transactions needed
   - Critical business data

✅ **Flexible Schema**
   - Data structure changes frequently
   - Rapid development
   - Agile environment

✅ **High Write Throughput**
   - IoT data ingestion
   - Real-time data collection
   - Logging

### 11.2 Use Elasticsearch When:

✅ **Full-Text Search**
   - Pencarian teks yang advanced
   - Relevance scoring needed
   - Fuzzy matching required

✅ **Search-Heavy Applications**
   - E-commerce search
   - Content search
   - Log search

✅ **Analytics**
   - Data aggregation
   - Metrics calculation
   - Business intelligence

✅ **Large-Scale Search**
   - Millions of documents
   - High search volume
   - Complex queries

### 11.3 Use Both When:

✅ **Need Both CRUD and Search**
   - Fast CRUD operations
   - Fast search operations
   - Best performance

✅ **Production Applications**
   - High traffic
   - Good user experience
   - Scalable architecture

✅ **Modern Applications**
   - Microservices architecture
   - API-first design
   - Cloud-native

**This Project**: ✅ Use Both
- MongoDB: Primary data storage
- Elasticsearch: Search index
- Best of both worlds

---

## 12. Project Implementation

### 12.1 MongoDB Role

```python
# Primary database
# Source of truth
# All CRUD operations

class MongoService:
    def insert_satu(self, produk):
        collection = self.dapatkan_koleksi()
        collection.insert_one(produk)
    
    def cari_semua(self):
        collection = self.dapatkan_koleksi()
        return list(collection.find({}))
    
    def update_data(self, produk_id, data_baru):
        collection = self.dapatkan_koleksi()
        collection.update_one(
          {"_id": produk_id},
          {"$set": data_baru}
        )
    
    def delete_data(self, produk_id):
        collection = self.dapatkan_koleksi()
        collection.delete_one({"_id": produk_id})
```

### 12.2 Elasticsearch Role

```python
# Search index
# Fast full-text search
# Synced from MongoDB

class ElasticService:
    def index_satu(self, produk):
        doc_id = produk["_id"]
        doc_body = {k: v for k, v in produk.items() if k != "_id"}
        
        client.index(
            index="produk",
            id=doc_id,
            body=doc_body
        )
    
    def cari_match(self, keyword):
        query = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["nama", "kategori", "spesifikasi"]
                }
            }
        }
        
        response = client.search(index="produk", body=query)
        return [hit["_source"] for hit in response["hits"]["hits"]]
```

### 12.3 Synchronization

```python
# Core Service syncs MongoDB → Elasticsearch

async def create_product(product):
    # 1. Insert to MongoDB
    mongo.insert_satu(product)
    
    # 2. Sync to Elasticsearch (async)
    asyncio.create_task(
        sync_to_search_service("POST", "/sync/single", product)
    )
    
    # 3. Return success
    return {"status": "success"}
```

---

## Summary

### Key Differences

| Aspect | MongoDB | Elasticsearch |
|--------|---------|---------------|
| **Purpose** | CRUD & Storage | Search & Analytics |
| **Best For** | Data operations | Text search |
| **Speed (CRUD)** | Very Fast | Limited |
| **Speed (Search)** | Slow | Very Fast |
| **Consistency** | Strong | Eventual |
| **Schema** | Flexible | Mapping required |

### Why Both in This Project?

1. **Complementary**: Each excels at different tasks
2. **Performance**: Best performance for both CRUD and search
3. **User Experience**: Fast operations across the board
4. **Scalability**: Can scale independently
5. **Best Practices**: Industry-standard architecture

### Conclusion

**MongoDB**: Primary database untuk CRUD  
**Elasticsearch**: Search engine untuk full-text search  
**Together**: Best performance dan user experience