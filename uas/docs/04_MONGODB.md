# MONGODB

## Apa itu NoSQL?

### Definisi
NoSQL (Not Only SQL) adalah kategori database management system yang tidak menggunakan model relasional tradisional. NoSQL dirancang untuk handling large-scale data yang memerlukan fleksibilitas schema, high performance, dan horizontal scalability.

### Perbedaan SQL vs NoSQL

| Aspek | SQL (Relational) | NoSQL (Non-Relational) |
|-------|------------------|------------------------|
| **Schema** | Fixed schema (tables, columns) | Flexible schema (documents, key-value) |
| **Data Model** | Tabular (rows & columns) | Document, Key-Value, Graph, Column |
| **Scaling** | Vertical (bigger server) | Horizontal (more servers) |
| **Joins** | Supported (INNER, LEFT, RIGHT) | Limited atau tidak ada |
| **Transactions** | ACID compliant | BASE (Eventually consistent) |
| **Query Language** | SQL (Standardized) | Varies by database |
| **Performance** | Good untuk complex queries | Excellent untuk simple operations |
| **Use Case** | Complex relationships, transactions | Large scale, flexible data |

### Kapan Menggunakan NoSQL?
✅ Data structure berubah-ubah  
✅ High write throughput dibutuhkan  
✅ Horizontal scaling diperlukan  
✅ Rapid prototyping  
✅ Big data applications  
✅ Real-time applications  
✅ Content management systems  
✅ IoT dan time-series data  

### Kapan Menggunakan SQL?
✅ Complex relationships antar data  
✅ ACID transactions critical  
✅ Data consistency paramount  
✅ Complex queries dengan JOIN  
✅ Structured data yang stabil  

---

## Konsep Dasar MongoDB

### 1. Database
- Container untuk collections
- Isolated dari database lain
- Bisa memiliki multiple collections
- Example: `uas_db`, `production_db`

```javascript
// Switch database
use uas_db

// Show databases
show dbs

// Drop database
db.dropDatabase()
```

### 2. Collection
- Group of documents (setara dengan table di SQL)
- Schema-less - setiap document bisa berbeda
- Tidak perlu define schema terlebih dahulu
- Example: `products`, `users`, `orders`

```javascript
// Show collections
show collections

// Create collection (implicit - otomatis saat insert)
db.products.insertOne({nama: "Laptop"})

// Create collection (explicit)
db.createCollection("products")
```

### 3. Document
- Unit dasar data (setara dengan row di SQL)
- Format: JSON-like (BSON - Binary JSON)
- Unique identifier: `_id` (ObjectId)
- Bisa memiliki nested documents dan arrays

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nama": "Laptop Asus ROG Zephyrus G14",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": {
    "processor": "AMD Ryzen 9",
    "ram": "16GB",
    "storage": "SSD 512GB",
    "gpu": "RTX 3060"
  },
  "tags": ["gaming", "high-performance", "amd"],
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-20T14:22:00Z")
}
```

### 4. ObjectId
- Unique identifier untuk setiap document
- 12-byte hexadecimal string
- Structure:
  - 4 bytes: Timestamp
  - 5 bytes: Machine identifier
  - 3 bytes: Process ID
  - 2 bytes: Counter

```javascript
// Generate ObjectId
ObjectId()

// Extract timestamp dari ObjectId
ObjectId("507f1f77bcf86cd799439011").getTimestamp()

// Convert ke string
ObjectId("507f1f77bcf86cd799439011").toString()
```

### 5. Data Types
```javascript
{
  // String
  "nama": "Laptop",  // "Laptop"
  
  // Number (Integer)
  "harga": 18999000,  // 18999000
  
  // Number (Float)
  "rating": 4.5,  // 4.5
  
  // Boolean
  "aktif": true,  // true
  
  // Array
  "tags": ["gaming", "laptop"],  // ["gaming", "laptop"]
  
  // Nested Document
  "spesifikasi": {
    "ram": "16GB",
    "processor": "Ryzen 9"
  },
  
  // Null
  "deskripsi": null,  // null
  
  // Date
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  
  // ObjectId
  "_id": ObjectId("507f1f77bcf86cd799439011")
}
```

---

## CRUD Operations

### CREATE (Insert)

#### insertOne()
```javascript
// Insert single document
db.products.insertOne({
  nama: "Laptop Asus ROG",
  kategori: "Laptop",
  harga: 18999000,
  stok: 15
})

// Result
{
  "acknowledged": true,
  "insertedId": ObjectId("507f1f77bcf86cd799439011")
}
```

#### insertMany()
```javascript
// Insert multiple documents
db.products.insertMany([
  {nama: "Laptop 1", harga: 5000000},
  {nama: "Laptop 2", harga: 6000000},
  {nama: "Laptop 3", harga: 7000000}
])

// Result
{
  "acknowledged": true,
  "insertedIds": [
    ObjectId("..."),
    ObjectId("..."),
    ObjectId("...")
  ]
}
```

### READ (Query)

#### find()
```javascript
// Find all documents
db.products.find()

// Find with filter
db.products.find({kategori: "Laptop"})

// Find with projection (select specific fields)
db.products.find(
  {kategori: "Laptop"},
  {nama: 1, harga: 1, _id: 0}
)

// Find with limit
db.products.find().limit(10)

// Find with skip (pagination)
db.products.find().skip(10).limit(10)

// Find with sort
db.products.find().sort({harga: -1})  // -1: desc, 1: asc

// Find one
db.products.findOne({_id: ObjectId("507f1f77bcf86cd799439011")})
```

#### Query Operators
```javascript
// Comparison operators
db.products.find({harga: {$gt: 10000000}})    // Greater than
db.products.find({harga: {$gte: 10000000}})   // Greater than or equal
db.products.find({harga: {$lt: 5000000}})     // Less than
db.products.find({harga: {$lte: 5000000}})    // Less than or equal
db.products.find({harga: {$ne: 5000000}})     // Not equal
db.products.find({kategori: {$in: ["Laptop", "Phone"]}})  // In array
db.products.find({kategori: {$nin: ["Laptop", "Phone"]}}) // Not in array

// Logical operators
db.products.find({
  $and: [
    {harga: {$gt: 5000000}},
    {stok: {$gt: 0}}
  ]
})

db.products.find({
  $or: [
    {kategori: "Laptop"},
    {kategori: "Phone"}
  ]
})

db.products.find({
  $not: {harga: {$lt: 1000000}}
})

// Element operators
db.products.find({tags: {$exists: true}})
db.products.find({harga: {$type: "int"}})
```

### UPDATE

#### updateOne()
```javascript
// Update single document
db.products.updateOne(
  {_id: ObjectId("507f1f77bcf86cd799439011")},
  {$set: {harga: 20000000, stok: 20}}
)

// Update with upsert (insert if not exists)
db.products.updateOne(
  {_id: ObjectId("507f1f77bcf86cd799439011")},
  {$set: {harga: 20000000}},
  {upsert: true}
)
```

#### updateMany()
```javascript
// Update multiple documents
db.products.updateMany(
  {kategori: "Laptop"},
  {$set: {diskon: 10}}
)

// Increment operator
db.products.updateOne(
  {_id: ObjectId("...")},
  {$inc: {stok: -5}}  // stok = stok - 5
)

// Rename field
db.products.updateMany(
  {},
  {$rename: {"old_field": "new_field"}}
)

// Remove field
db.products.updateMany(
  {},
  {$unset: {field_to_remove: ""}}
)

// Array operators
db.products.updateOne(
  {_id: ObjectId("...")},
  {$push: {tags: "new-tag"}}
)

db.products.updateOne(
  {_id: ObjectId("...")},
  {$addToSet: {tags: "unique-tag"}}  // Only if not exists
)
```

### DELETE

#### deleteOne()
```javascript
// Delete single document
db.products.deleteOne({_id: ObjectId("507f1f77bcf86cd799439011")})

// Result
{ "acknowledged": true, "deletedCount": 1 }
```

#### deleteMany()
```javascript
// Delete multiple documents
db.products.deleteMany({kategori: "Laptop"})

// Delete all documents
db.products.deleteMany({})
```

---

## Aggregation Pipeline

Aggregation pipeline adalah framework untuk data transformation dan analysis. Consists dari multiple stages:

```javascript
db.products.aggregate([
  // Stage 1: Filter documents
  {$match: {kategori: "Laptop"}},
  
  // Stage 2: Group by category
  {$group: {
    _id: "$kategori",
    total_produk: {$sum: 1},
    total_stok: {$sum: "$stok"},
    rata_harga: {$avg: "$harga"},
    harga_tertinggi: {$max: "$harga"},
    harga_terendah: {$min: "$harga"}
  }},
  
  // Stage 3: Sort by total_stok descending
  {$sort: {total_stok: -1}},
  
  // Stage 4: Limit to top 5
  {$limit: 5},
  
  // Stage 5: Project (select fields)
  {$project: {
    _id: 0,
    kategori: "$_id",
    total_produk: 1,
    total_stok: 1,
    rata_harga: {$round: ["$rata_harga", 0]}
  }}
])
```

### Common Aggregation Stages

#### $match
Filter documents (seperti WHERE di SQL)
```javascript
{$match: {harga: {$gt: 10000000}}}
```

#### $group
Group documents dan calculate aggregates
```javascript
{$group: {
  _id: "$kategori",
  total: {$sum: "$stok"}
}}
```

#### $project
Select/rename fields
```javascript
{$project: {
  nama: 1,
  harga: 1,
  _id: 0
}}
```

#### $sort
Sort documents
```javascript
{$sort: {harga: -1}}  // -1: desc, 1: asc
```

#### $limit
Limit number of documents
```javascript
{$limit: 10}
```

#### $skip
Skip documents (untuk pagination)
```javascript
{$skip: 10}
```

#### $lookup
Join collections (seperti LEFT JOIN)
```javascript
{$lookup: {
  from: "categories",
  localField: "kategori_id",
  foreignField: "_id",
  as: "kategori"
}}
```

---

## Regex Search

MongoDB mendukung regex search untuk pattern matching:

```javascript
// Case-insensitive search
db.products.find({
  nama: {$regex: "laptop", $options: "i"}
})

// Search di multiple fields
db.products.find({
  $or: [
    {nama: {$regex: "laptop", $options: "i"}},
    {kategori: {$regex: "laptop", $options: "i"}},
    {spesifikasi: {$regex: "laptop", $options: "i"}}
  ]
})

// Starts with
db.products.find({
  nama: {$regex: "^laptop", $options: "i"}
})

// Ends with
db.products.find({
  nama: {$regex: "gaming$", $options: "i"}
})
```

### Kekurangan Regex Search
❌ Full collection scan (slow untuk large datasets)  
❌ Tidak ada relevance scoring  
❌ Tidak ada fuzzy matching  
❌ Tidak ada stemming (laptop ≠ laptops)  
❌ CPU intensive  

---

## Indexing

Index meningkatkan performa query dengan membuat data structure untuk fast lookup:

```javascript
// Create single field index
db.products.createIndex({nama: 1})

// Create compound index
db.products.createIndex({kategori: 1, harga: -1})

// Create unique index
db.products.createIndex({email: 1}, {unique: true})

// Create text index (for text search)
db.products.createIndex({
  nama: "text",
  kategori: "text",
  spesifikasi: "text"
})

// Text search
db.products.find({
  $text: {$search: "laptop gaming"}
})

// List all indexes
db.products.getIndexes()

// Drop index
db.products.dropIndex("nama_1")

// Explain query performance
db.products.find({nama: "Laptop"}).explain("executionStats")
```

---

## Kelebihan MongoDB

✅ **Schema Flexibility**: Document bisa memiliki structure berbeda  
✅ **Horizontal Scalability**: Sharding untuk distribusi data  
✅ **High Write Performance**: Optimized untuk write operations  
✅ **Rich Query Language**: Powerful query dan aggregation  
✅ **Built-in Replication**: High availability dengan replica sets  
✅ **JSON-like Format**: Native untuk web applications  
✅ **Rapid Prototyping**: Quick development tanpa schema migration  
✅ **Aggregation Framework**: Powerful data transformation  
✅ **GridFS**: Store large files (images, videos)  
✅ **TTL Indexes**: Auto-delete expired data  

---

## Kekurangan MongoDB

❌ **No JOIN Support**: Tidak ada native JOIN (perlu embedding atau manual)  
❌ **Memory Usage**: High memory untuk large datasets  
❌ **Eventual Consistency**: Bisa ada delay dalam replication  
❌ **Storage Overhead**: Lebih banyak storage dibanding SQL  
❌ **Not for Complex Relations**: Tidak cocok untuk complex relational data  
❌ **Transaction Complexity**: Multi-document transactions baru di v4.0  
❌ **Learning Curve**: Aggregation framework kompleks  
❌ **No ACID by Default**: Sebelum v4.0, transactions tidak complete  

---

## MongoDB dalam Project Ini

### Role
- **Primary Database**: Menyimpan semua data produk
- **CRUD Operations**: Create, Read, Update, Delete products
- **Data Source**: Sumber data utama untuk aplikasi

### Schema Design
```json
{
  "_id": 1,  // Integer ID (bukan ObjectId) untuk simplicity
  "nama": "Laptop Asus ROG Zephyrus G14",
  "kategori": "Laptop",
  "harga": 18999000,
  "stok": 15,
  "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
}
```

### Mengapa Integer _id instead of ObjectId?
- **Simplicity**: Lebih mudah dibaca dan debug
- **Performance**: Integer lebih cepat untuk comparison
- **Compatibility**: Lebih mudah di-integrasikan dengan Elasticsearch
- **Use Case**: Data produk dengan ID yang pre-defined

### Operations in Project
```python
# CREATE
collection.insert_one(produk_dict)

# READ ALL
collection.find({})

# READ BY ID
collection.find_one({"_id": product_id})

# UPDATE
collection.update_one(
  {"_id": product_id},
  {"$set": data_baru}
)

# DELETE
collection.delete_one({"_id": product_id})
```

### Performance Optimization
- **Index pada _id**: Automatic primary key index
- **Connection Pooling**: Reuse MongoDB connections
- **Projection**: Select only needed fields
- **Batch Operations**: insert_many() untuk bulk insert

---

## MongoDB Diagram

```
┌─────────────────────────────────────────┐
│         MongoDB (uas_db)                │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Collection: products            │  │
│  │                                   │  │
│  │  Document 1:                      │  │
│  │  {                                │  │
│  │    "_id": 1,                      │  │
│  │    "nama": "Laptop Asus",         │  │
│  │    "harga": 18999000,             │  │
│  │    "stok": 15                     │  │
│  │  }                                │  │
│  │                                   │  │
│  │  Document 2:                      │  │
│  │  {                                │  │
│  │    "_id": 2,                      │  │
│  │    "nama": "iPhone 15",           │  │
│  │    "harga": 25000000,             │  │
│  │    "stok": 8                      │  │
│  │  }                                │  │
│  │                                   │  │
│  │  ...                              │  │
│  │  Document N                       │  │
│  │  {                                │  │
│  │    "_id": N,                      │  │
│  │    "nama": "...",                 │  │
│  │    "harga": ...,                  │  │
│  │    "stok": ...                    │  │
│  │  }                                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘

Index:
  - _id (Primary Key - Automatic)
```

---

## MongoDB Commands Reference

### Database Commands
```bash
# Show databases
show dbs

# Use database
use uas_db

# Show collections
show collections

# Drop database
db.dropDatabase()
```

### Collection Commands
```bash
# Create collection
db.createCollection("products")

# Drop collection
db.products.drop()

# Rename collection
db.products.rename("items")
```

### Query Commands
```bash
# Find all
db.products.find()

# Find with filter
db.products.find({kategori: "Laptop"})

# Find one
db.products.findOne({_id: 1})

# Count
db.products.countDocuments({kategori: "Laptop"})

# Distinct
db.products.distinct("kategori")
```

### Index Commands
```bash
# Create index
db.products.createIndex({nama: 1})

# List indexes
db.products.getIndexes()

# Drop index
db.products.dropIndex("nama_1")

# Explain query
db.products.find({nama: "Laptop"}).explain("executionStats")
```

### Import/Export
```bash
# Import JSON
mongoimport --db uas_db --collection products --file products.json --jsonArray

# Export JSON
mongoexport --db uas_db --collection products --out products.json --jsonArray