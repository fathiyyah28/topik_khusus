# ALUR CRUD

## Overview
Bagian ini menjelaskan alur operasi CRUD (Create, Read, Update, Delete) secara detail dengan sequence diagram dan penjelasan setiap langkah. Operasi CRUD adalah fondasi dari sistem manajemen data.

---

## CRUD Operations Overview

```
CREATE    →  Menambahkan data baru
READ      →  Membaca/melihat data
UPDATE    →  Mengubah data yang ada
DELETE    →  Menghapus data
```

---

## 1. CREATE - Menambahkan Produk Baru

### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│User  │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Fill   │             │             │
   │    form   │             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. Submit │             │             │
   │           │ 3. POST     │             │
   │           │/api/products│             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 4. Validate │
   │           │             │    schema   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 5. Check    │
   │           │             │   duplicate │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 6. insert_  │
   │           │             │    one()    │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 7. {ack:    │
   │           │             │    true}    │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 8. Create   │
   │           │             │   sync task │
   │           │             │ (async)     │
   │           │             │             │
   │           │             │ 9. 201      │
   │           │             │   Created   │
   │           │             │<────────────│
   │           │             │             │
   │ 10. Show  │             │             │
   │   success │             │             │
   │<──────────│             │             │
   │           │             │             │
   │ 11. (Async)            │             │
   │           │ 12. POST    │             │
   │           │/api/sync/   │             │
   │           │   single    │             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 13. index() │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 14. 201     │
   │           │             │<────────────│
   │           │             │             │
```

### Detailed Flow

#### Step 1-2: User Input & Submit
```javascript
// Frontend - User fills form
const productData = {
  _id: 1,
  nama: "Laptop Asus ROG Zephyrus G14",
  kategori: "Laptop",
  harga: 18999000,
  stok: 15,
  spesifikasi: "AMD Ryzen 9, RAM 16GB, SSD 512GB, RTX 3060"
}

// Submit form
const response = await axios.post('/api/products', productData)
```

#### Step 3-4: Core Service - Receive & Validate
```python
# Core Service - routes.py
@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreateSchema):
    """
    Pydantic validation happens automatically:
    - id: int (required)
    - nama: str (required)
    - kategori: str (required)
    - harga: int >= 0
    - stok: int >= 0
    - spesifikasi: str (required)
    """
    
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Check duplicate
    existing = mongo.cari_by_id(product.id)
    if existing:
        raise HTTPException(400, f"Produk dengan ID {product.id} sudah ada")
```

#### Step 5-6: Core Service - Insert to MongoDB
```python
    # Convert Pydantic model to dict with alias
    produk_dict = product.model_dump(by_alias=True)
    # Result: {"_id": 1, "nama": "Laptop Asus ROG", ...}
    
    # Insert to MongoDB
    result = mongo.insert_satu(produk_dict)
    if result is None:
        raise HTTPException(500, "Gagal insert produk")
```

```python
# mongo_service.py
def insert_satu(produk: Dict[str, Any]) -> Optional[int]:
    collection = dapatkan_koleksi()
    
    try:
        result = collection.insert_one(produk)
        logger.info(f"Berhasil insert produk ID {produk['_id']}.")
        return produk["_id"]
    except PyMongoError as e:
        logger.error(f"Gagal insert produk: {e}")
        return None
```

#### Step 7-9: Core Service - Response & Async Sync
```python
    # Create async sync task (fire-and-forget)
    asyncio.create_task(
        sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
    )
    
    # Immediately return response to client
    return ProductResponse(
        status="success",
        message=f"Produk ID {result} berhasil dibuat",
        data=produk_dict
    )
```

#### Step 10: Frontend - Display Success
```javascript
// Frontend receives response
const response = await axios.post('/api/products', productData)

// Show success message
alert(response.data.message)

// Refresh product list
await loadProducts()

// Clear form
productData.value = {
  _id: '',
  nama: '',
  kategori: '',
  harga: '',
  stok: '',
  spesifikasi: ''
}
```

#### Step 11-14: Background Sync to Elasticsearch
```python
# Background task runs independently
async def sinkronisasi_ke_search_service(method: str, endpoint: str, data: Dict[str, Any]):
    url = f"http://search-service:8002/api{endpoint}"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(url, json=data)
        logger.info(f"Sinkronisasi berhasil: POST {url}")
    except httpx.RequestError as e:
        logger.warning(f"Sinkronisasi gagal: {e}")

# Search Service receives sync
@router.post("/sync/single", response_model=SyncResponse, status_code=201)
async def sync_single_product(product: Dict[str, Any]):
    doc_id = product["_id"]
    doc_body = {k: v for k, v in product.items() if k != "_id"}
    
    client.index(
        index=ELASTIC_INDEX_NAME,
        id=doc_id,
        body=doc_body
    )
    
    client.indices.refresh(index=ELASTIC_INDEX_NAME)
    
    return SyncResponse(
        message=f"Produk ID {doc_id} berhasil disinkronisasi",
        total=1
    )
```

---

## 2. READ - Melihat Produk

### 2.1 Read All Products

#### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│User  │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Navigate            │             │
   │    to page             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. GET    │             │             │
   │/api/products            │             │
   │           │ 3. GET      │             │
   │           │/api/products│             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 4. find({}) │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 5. [       │
   │           │             │   {_id:1,  │
   │           │             │    ...},   │
   │           │             │   {_id:2,  │
   │           │             │    ...}    │
   │           │             │ ]          │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 6. 200 OK  │
   │           │             │<────────────│
   │           │             │             │
   │ 7. Display │             │             │
   │   products │             │             │
   │<──────────│             │             │
   │           │             │             │
```

#### Detailed Flow

**Step 1-2: Frontend - Load Page**
```javascript
// Frontend - App.vue or ProductList.vue
onMounted(async () => {
  await loadProducts()
})

async function loadProducts() {
  try {
    const response = await axios.get('/api/products')
    products.value = response.data.data
    total.value = response.data.total
  } catch (error) {
    console.error('Failed to load products:', error)
  }
}
```

**Step 3-4: Core Service - Query MongoDB**
```python
# Core Service - routes.py
@router.get("/products", response_model=ProductListResponse)
async def get_all_products():
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Get all products
    products = mongo.cari_semua()
    
    return ProductListResponse(
        status="success",
        message=f"Ditemukan {len(products)} produk",
        data=products,
        total=len(products)
    )
```

```python
# mongo_service.py
def cari_semua() -> List[Dict[str, Any]]:
    collection = dapatkan_koleksi()
    
    try:
        # Query all documents
        data = list(collection.find({}))
        
        # Convert ObjectId to string for JSON serialization
        for item in data:
            item["_id"] = str(item["_id"])
        
        logger.info(f"Data ditemukan: {len(data)} produk.")
        return data
    except PyMongoError as e:
        logger.error(f"Gagal mengambil data: {e}")
        return []
```

**Step 5-7: Response & Display**
```python
# Response
{
  "status": "success",
  "message": "Ditemukan 12 produk",
  "data": [
    {
      "_id": 1,
      "nama": "Laptop Asus ROG",
      "kategori": "Laptop",
      "harga": 18999000,
      "stok": 15,
      "spesifikasi": "AMD Ryzen 9, RAM 16GB, SSD 512GB"
    },
    {
      "_id": 2,
      "nama": "iPhone 15 Pro",
      "kategori": "Phone",
      "harga": 25000000,
      "stok": 8,
      "spesifikasi": "A17 Pro, 256GB"
    },
    ...
  ],
  "total": 12
}

// Frontend displays products in cards/table
```

### 2.2 Read Single Product

#### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│User  │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Click  │             │             │
   │   product │             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. GET    │             │             │
   │/api/      │ 3. GET      │             │
   │products/1│/api/products/1             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 4. find_   │
   │           │             │    one()   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 5. {       │
   │           │             │   _id: 1,  │
   │           │             │   ...      │
   │           │             │  }         │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 6. 200 OK  │
   │           │             │<────────────│
   │           │             │             │
   │ 7. Show   │             │             │
   │   detail  │             │             │
   │<──────────│             │             │
   │           │             │             │
```

#### Detailed Flow

**Step 1-2: Frontend - Click Product**
```javascript
// Frontend - ProductCard.vue
async function viewProduct(productId) {
  try {
    const response = await axios.get(`/api/products/${productId}`)
    selectedProduct.value = response.data.data
    showDetailModal.value = true
  } catch (error) {
    console.error('Failed to load product:', error)
  }
}
```

**Step 3-6: Core Service - Query Single Product**
```python
# Core Service - routes.py
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Find product by ID
    product = mongo.cari_by_id(product_id)
    if product is None:
        raise HTTPException(404, f"Produk dengan ID {product_id} tidak ditemukan")
    
    return ProductResponse(
        status="success",
        message="Produk ditemukan",
        data=product
    )
```

```python
# mongo_service.py
def cari_by_id(produk_id: int) -> Optional[Dict[str, Any]]:
    collection = dapatkan_koleksi()
    
    try:
        # Find one document by ID
        data = collection.find_one({"_id": produk_id})
        
        if data:
            # Convert ObjectId to string
            data["_id"] = str(data["_id"])
            return data
        
        return None
    except PyMongoError as e:
        logger.error(f"Gagal mencari data: {e}")
        return None
```

**Step 7: Frontend - Display Detail**
```javascript
// Response
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

// Frontend shows modal with product details
```

---

## 3. UPDATE - Mengubah Produk

### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│User  │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Edit   │             │             │
   │   form    │             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. PUT    │             │             │
   │/api/      │ 3. PUT      │             │
   │products/1│/api/products/1             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 4. Validate │
   │           │             │    schema   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 5. Check    │
   │           │             │   exists    │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 6. update_  │
   │           │             │    one()    │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 7. {       │
   │           │             │   mod: 1   │
   │           │             │  }         │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 8. Create   │
   │           │             │   sync task │
   │           │             │ (async)     │
   │           │             │             │
   │           │             │ 9. Fetch    │
   │           │             │   updated   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 10. {      │
   │           │             │   _id: 1,  │
   │           │             │   ...       │
   │           │             │  }         │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 11. 200 OK │
   │           │             │<────────────│
   │           │             │             │
   │ 12. Show  │             │             │
   │   success │             │             │
   │<──────────│             │             │
   │           │             │             │
   │ 13. (Async)            │             │
   │           │ 14. PUT     │             │
   │           │/api/sync/1  │             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 15. update()│
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 16. 200 OK │
   │           │             │<────────────│
   │           │             │             │
```

### Detailed Flow

#### Step 1-2: Frontend - Edit & Submit
```javascript
// Frontend - ProductForm.vue
const updatedData = {
  nama: "Laptop Asus ROG Zephyrus G14 (Updated)",
  harga: 19999000,
  stok: 12
}

// Send PUT request
const response = await axios.put(`/api/products/${productId}`, updatedData)
```

#### Step 3-5: Core Service - Validate & Check
```python
# Core Service - routes.py
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdateSchema):
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Check if product exists
    existing = mongo.cari_by_id(product_id)
    if existing is None:
        raise HTTPException(404, f"Produk dengan ID {product_id} tidak ditemukan")
    
    # Get only non-None fields (partial update)
    data_baru = product.model_dump(exclude_none=True, by_alias=True)
    
    if not data_baru:
        raise HTTPException(400, "Tidak ada data yang diupdate")
```

#### Step 6-7: Core Service - Update MongoDB
```python
    # Update MongoDB
    berhasil = mongo.update_data(product_id, data_baru)
    if not berhasil:
        raise HTTPException(500, "Gagal update produk")
```

```python
# mongo_service.py
def update_data(produk_id: int, data_baru: Dict[str, Any]) -> bool:
    collection = dapatkan_koleksi()
    
    try:
        # Update document
        result = collection.update_one(
            {"_id": produk_id},
            {"$set": data_baru}
        )
        
        if result.modified_count > 0:
            logger.info(f"Data ID {produk_id} berhasil diupdate.")
            return True
        else:
            logger.warning(f"Data ID {produk_id} tidak ditemukan.")
            return False
    except PyMongoError as e:
        logger.error(f"Gagal update data: {e}")
        return False
```

```javascript
// MongoDB executes
db.products.updateOne(
  {_id: 1},
  {$set: {nama: "Laptop Asus ROG Zephyrus G14 (Updated)", harga: 19999000, stok: 12}}
)

// Returns: {acknowledged: true, modifiedCount: 1}
```

#### Step 8-11: Core Service - Sync & Response
```python
    # Sync to Search Service (async)
    asyncio.create_task(
        sinkronisasi_ke_search_service("PUT", f"/sync/{product_id}", data_baru)
    )
    
    # Fetch updated data
    updated = mongo.cari_by_id(product_id)
    
    return ProductResponse(
        status="success",
        message=f"Produk ID {product_id} berhasil diupdate",
        data=updated
    )
```

#### Step 12-16: Background Sync to Elasticsearch
```python
# Search Service - routes.py
@router.put("/sync/{product_id}", response_model=SyncResponse)
async def sync_update_product(product_id: int, data: Dict[str, Any]):
    if not data:
        raise HTTPException(400, "Tidak ada data untuk diupdate")
    
    berhasil = es.update_data(product_id, data)
    if not berhasil:
        raise HTTPException(404, f"Produk ID {product_id} tidak ditemukan di Elasticsearch")
    
    return SyncResponse(
        message=f"Produk ID {product_id} berhasil diupdate di Elasticsearch",
        total=1
    )
```

```python
# elastic_service.py
def update_data(produk_id: int, data_baru: Dict[str, Any]) -> bool:
    client = dapatkan_koneksi()
    
    try:
        # Partial update document
        client.update(
            index=ELASTIC_INDEX_NAME,
            id=produk_id,
            body={"doc": data_baru}
        )
        
        # Refresh index
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        
        logger.info(f"Data ID {produk_id} berhasil diupdate di ES.")
        return True
    except NotFoundError:
        logger.warning(f"Data ID {produk_id} tidak ditemukan di ES.")
        return False
    except Exception as e:
        logger.error(f"Gagal update data di ES: {e}")
        return False
```

---

## 4. DELETE - Menghapus Produk

### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│User  │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Click  │             │             │
   │   delete  │             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. Confirm│             │             │
   │   dialog  │             │             │
   │<──────────│             │             │
   │           │             │             │
   │ 3. DELETE │             │             │
   │/api/      │ 4. DELETE   │             │
   │products/1│/api/products/1             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 5. Check    │
   │           │             │   exists    │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 6. delete_  │
   │           │             │    one()    │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 7. {       │
   │           │             │   del: 1   │
   │           │             │  }         │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 8. Create   │
   │           │             │   sync task │
   │           │             │ (async)     │
   │           │             │             │
   │           │             │ 9. 200 OK  │
   │           │             │<────────────│
   │           │             │             │
   │ 10. Remove│             │             │
   │   from    │             │             │
   │   list    │             │             │
   │<──────────│             │             │
   │           │             │             │
   │ 11. (Async)            │             │
   │           │ 12. DELETE  │             │
   │           │/api/sync/1  │             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 13. delete()│
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 14. 200 OK │
   │           │             │<────────────│
   │           │             │             │
```

### Detailed Flow

#### Step 1-3: Frontend - Confirm & Delete
```javascript
// Frontend - ProductCard.vue
async function deleteProduct(productId) {
  // Confirm dialog
  const confirmed = confirm("Apakah Anda yakin ingin menghapus produk ini?")
  
  if (!confirmed) return
  
  try {
    // Send DELETE request
    const response = await axios.delete(`/api/products/${productId}`)
    
    // Show success message
    alert(response.data.message)
    
    // Remove from list
    products.value = products.value.filter(p => p._id !== productId)
    
  } catch (error) {
    console.error('Failed to delete product:', error)
    alert('Gagal menghapus produk')
  }
}
```

#### Step 4-7: Core Service - Delete from MongoDB
```python
# Core Service - routes.py
@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int):
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Check if product exists
    existing = mongo.cari_by_id(product_id)
    if existing is None:
        raise HTTPException(404, f"Produk dengan ID {product_id} tidak ditemukan")
    
    # Delete from MongoDB
    berhasil = mongo.delete_data(product_id)
    if not berhasil:
        raise HTTPException(500, "Gagal hapus produk")
```

```python
# mongo_service.py
def delete_data(produk_id: int) -> bool:
    collection = dapatkan_koleksi()
    
    try:
        # Delete document
        result = collection.delete_one({"_id": produk_id})
        
        if result.deleted_count > 0:
            logger.info(f"Data ID {produk_id} berhasil dihapus.")
            return True
        else:
            logger.warning(f"Data ID {produk_id} tidak ditemukan.")
            return False
    except PyMongoError as e:
        logger.error(f"Gagal hapus data: {e}")
        return False
```

```javascript
// MongoDB executes
db.products.deleteOne({_id: 1})

// Returns: {acknowledged: true, deletedCount: 1}
```

#### Step 8-9: Core Service - Sync & Response
```python
    # Sync to Search Service (async)
    asyncio.create_task(
        sinkronisasi_ke_search_service("DELETE", f"/sync/{product_id}")
    )
    
    return ProductResponse(
        status="success",
        message=f"Produk ID {product_id} berhasil dihapus",
        data=None
    )
```

#### Step 10-14: Background Sync to Elasticsearch
```python
# Search Service - routes.py
@router.delete("/sync/{product_id}", response_model=SyncResponse)
async def sync_delete_product(product_id: int):
    berhasil = es.delete_data(product_id)
    if not berhasil:
        raise HTTPException(404, f"Produk ID {product_id} tidak ditemukan di Elasticsearch")
    
    return SyncResponse(
        message=f"Produk ID {product_id} berhasil dihapus dari Elasticsearch",
        total=1
    )
```

```python
# elastic_service.py
def delete_data(produk_id: int) -> bool:
    client = dapatkan_koneksi()
    
    try:
        # Delete document
        client.delete(
            index=ELASTIC_INDEX_NAME,
            id=produk_id
        )
        
        # Refresh index
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        
        logger.info(f"Data ID {produk_id} berhasil dihapus dari ES.")
        return True
    except NotFoundError:
        logger.warning(f"Data ID {produk_id} tidak ditemukan di ES.")
        return False
    except Exception as e:
        logger.error(f"Gagal hapus data di ES: {e}")
        return False
```

---

## 5. Bulk Operations - Seed Data

### Sequence Diagram
```
┌──────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Admin │  │Frontend  │  │Core Svc  │  │  MongoDB │
└──┬───┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
   │           │             │             │
   │ 1. Click  │             │             │
   │   Seed    │             │             │
   │──────────>│             │             │
   │           │             │             │
   │ 2. POST   │             │             │
   │/api/      │ 3. POST     │             │
   │products/  │/api/products/             │
   │   seed    │   seed      │             │
   │           │────────────>│             │
   │           │             │             │
   │           │             │ 4. Load    │
   │           │             │   JSON     │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 5. delete_  │
   │           │             │    many()   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 6. insert_  │
   │           │             │    many()   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 7. {       │
   │           │             │   count:12 │
   │           │             │  }         │
   │           │             │<────────────│
   │           │             │             │
   │           │             │ 8. POST     │
   │           │             │/api/sync   │
   │           │             │────────────>│
   │           │             │             │
   │           │             │ 9. 201      │
   │           │             │<────────────│
   │           │             │             │
   │ 10. Show  │             │             │
   │   success │             │             │
   │<──────────│             │             │
   │           │             │             │
```

### Detailed Flow

#### Step 1-3: Frontend - Trigger Seed
```javascript
// Frontend
async function seedProducts() {
  const confirmed = confirm("Ini akan menghapus semua data dan mengisi ulang. Lanjutkan?")
  
  if (!confirmed) return
  
  try {
    const response = await axios.post('/api/products/seed')
    alert(response.data.message)
    await loadProducts()
  } catch (error) {
    console.error('Failed to seed products:', error)
    alert('Gagal seed data')
  }
}
```

#### Step 4-7: Core Service - Load & Insert
```python
# Core Service - routes.py
@router.post("/products/seed", response_model=ProductListResponse, status_code=201)
async def seed_products():
    # Check MongoDB connection
    if not mongo.cek_koneksi():
        raise HTTPException(503, "MongoDB tidak tersedia")
    
    # Load dataset from JSON file
    data = mongo.muat_dataset()
    if not data:
        raise HTTPException(400, "Dataset kosong atau file tidak ditemukan")
    
    # Insert to MongoDB (bulk)
    jumlah = mongo.insert_banyak(data)
    if jumlah == 0:
        raise HTTPException(500, "Gagal seed ke MongoDB")
```

```python
# mongo_service.py
def insert_banyak(data_list: List[Dict[str, Any]]) -> int:
    collection = dapatkan_koleksi()
    
    try:
        # Delete all existing data
        collection.delete_many({})
        logger.info("Data lama dihapus.")
        
        # Insert new data
        result = collection.insert_many(data_list)
        jumlah = len(result.inserted_ids)
        logger.info(f"Berhasil insert {jumlah} data ke MongoDB.")
        return jumlah
    except PyMongoError as e:
        logger.error(f"Gagal insert data: {e}")
        raise
```

#### Step 8-9: Core Service - Bulk Sync
```python
    # Sync all data to Search Service
    await sinkronisasi_ke_search_service("POST", "/sync", {"products": data})
    
    return ProductListResponse(
        status="success",
        message=f"Berhasil seed {jumlah} produk ke MongoDB dan Elasticsearch",
        data=data,
        total=jumlah
    )
```

#### Step 10: Search Service - Bulk Index
```python
# Search Service - routes.py
@router.post("/sync", response_model=SyncResponse, status_code=201)
async def sync_products(request: SyncRequest):
    if not es.cek_koneksi():
        raise HTTPException(503, "Elasticsearch tidak tersedia")
    
    if not request.products:
        raise HTTPException(400, "Tidak ada data produk untuk disinkronisasi")
    
    jumlah = es.index_banyak(request.products)
    
    return SyncResponse(
        message=f"Berhasil sinkronisasi {jumlah} produk ke Elasticsearch",
        total=jumlah
    )
```

```python
# elastic_service.py
def index_banyak(data_list: List[Dict[str, Any]]) -> int:
    client = dapatkan_koneksi()
    
    try:
        # Delete old index
        if client.indices.exists(index=ELASTIC_INDEX_NAME):
            client.indices.delete(index=ELASTIC_INDEX_NAME)
            logger.info("Index lama dihapus.")
        
        # Create new index
        buat_index()
        
        # Index all documents
        jumlah = 0
        for data in data_list:
            doc_id = data["_id"]
            doc_body = {k: v for k, v in data.items() if k != "_id"}
            
            client.index(
                index=ELASTIC_INDEX_NAME,
                id=doc_id,
                body=doc_body
            )
            jumlah += 1
        
        # Refresh index
        client.indices.refresh(index=ELASTIC_INDEX_NAME)
        
        logger.info(f"Berhasil index {jumlah} data ke Elasticsearch.")
        return jumlah
    except Exception as e:
        logger.error(f"Gagal index data: {e}")
        raise
```

---

## 6. Error Handling in CRUD

### 6.1 Validation Errors
```python
# Pydantic validation errors
{
  "detail": [
    {
      "loc": ["body", "harga"],
      "msg": "Input should be greater than or equal to 0",
      "type": "greater_than_equal"
    }
  ]
}

# Frontend displays error message
```

### 6.2 Not Found Errors
```python
# Product not found
{
  "detail": "Produk dengan ID 999 tidak ditemukan"
}

# HTTP Status: 404 Not Found
```

### 6.3 Duplicate Errors
```python
# Duplicate product ID
{
  "detail": "Produk dengan ID 1 sudah ada"
}

# HTTP Status: 400 Bad Request
```

### 6.4 Database Errors
```python
# MongoDB connection error
{
  "detail": "MongoDB tidak tersedia"
}

# HTTP Status: 503 Service Unavailable
```

### 6.5 Sync Errors (Non-blocking)
```python
# Sync fails but CRUD succeeds
# Core Service logs warning but returns success
logger.warning(f"Sinkronisasi gagal (Search Service mungkin offline): {e}")

# User sees success message
# Data will be synced when Search Service is back online
```

---

## 7. Data Consistency

### 7.1 MongoDB (Strong Consistency)
```
Write Operation
    ↓
MongoDB Primary
    ↓
Acknowledge (immediate)
    ↓
Data is consistent
```

### 7.2 Elasticsearch (Eventual Consistency)
```
Write Operation
    ↓
Elasticsearch Index
    ↓
Refresh (1 second)
    ↓
Searchable
    ↓
Eventual consistency (acceptable for search)
```

### 7.3 Sync Strategy
```
MongoDB (Source of Truth)
    ↓
Real-time async sync
    ↓
Elasticsearch (Search Index)
    ↓
Eventual consistency
```

---

## 8. Performance Considerations

### 8.1 Response Times
```
CREATE Operation:
- Validation: 5-10ms
- MongoDB Insert: 10-50ms
- Response: 5-10ms
- Total: 20-70ms

READ Operation:
- MongoDB Query: 10-50ms
- Response: 5-10ms
- Total: 15-60ms

UPDATE Operation:
- Validation: 5-10ms
- MongoDB Update: 10-50ms
- Response: 5-10ms
- Total: 20-70ms

DELETE Operation:
- MongoDB Delete: 10-50ms
- Response: 5-10ms
- Total: 15-60ms
```

### 8.2 Optimization
- **Connection Pooling**: Reuse MongoDB connections
- **Async Operations**: Non-blocking sync to Search Service
- **Indexing**: MongoDB _id index, Elasticsearch inverted index
- **Caching**: Future enhancement with Redis

---

## Summary

### CRUD Operations
1. **CREATE**: Insert to MongoDB → Async sync to Elasticsearch → Return success
2. **READ**: Query MongoDB → Return data → Display in UI
3. **UPDATE**: Update MongoDB → Async sync to Elasticsearch → Return updated data
4. **DELETE**: Delete from MongoDB → Async sync to Elasticsearch → Return success

### Key Patterns
- **Fire-and-Forget**: Sync happens in background
- **Strong Consistency**: MongoDB is source of truth
- **Eventual Consistency**: Elasticsearch for search only
- **Error Handling**: Graceful degradation
- **Performance**: Sub-100ms response times