# PERMASALAHAN DAN SOLUSI

## Overview
Bagian ini menjelaskan permasalahan yang dihadapi selama pengembangan project dan solusi yang diterapkan untuk mengatasinya.

---

## PERMASALAHAN 1: Pencarian Data yang Lambat

### Deskripsi
Sistem menggunakan regex MongoDB untuk pencarian produk. Ketika data mencapai ribuan record, performa pencarian menurun drastis karena MongoDB harus melakukan full collection scan.

### Dampak
- Waktu respons pencarian > 2 detik untuk 10,000 produk
- CPU usage tinggi pada MongoDB server
- User experience yang buruk
- Tidak scalable untuk pertumbuhan data

### Solusi
Mengimplementasikan Elasticsearch sebagai search engine terpisah:
- **Inverted Index**: Pencarian O(1) instead of O(n)
- **Full-Text Search**: Analisis token dan stemming
- **Relevance Scoring**: Hasil diurutkan berdasarkan relevansi
- **Performance**: Pencarian < 100ms untuk 1 juta dokumen

### Implementasi
```python
# Search Service menggunakan Elasticsearch
def cari_match(keyword: str) -> List[Dict[str, Any]]:
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["nama", "kategori", "spesifikasi"],
                "type": "best_fields"
            }
        }
    }
    response = client.search(index=ELASTIC_INDEX_NAME, body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]
```

---

## PERMASALAHAN 2: Monolith Architecture

### Deskripsi
Semua fungsi (CRUD, Search, Business Logic) berada dalam satu aplikasi backend. Sulit untuk maintenance, testing, dan scaling.

### Dampak
- Codebase yang besar dan kompleks
- Sulit di-scale secara independen
- Single point of failure
- Deployment yang riskan (semua atau tidak sama sekali)
- Sulit untuk kolaborasi tim

### Solusi
Mengadopsi arsitektur Microservices:
- **Core Service**: CRUD operations dengan MongoDB
- **Search Service**: Search operations dengan Elasticsearch
- **Frontend**: User interface dengan Vue.js

### Keuntungan
- Independent scaling (Core bisa di-scale terpisah dari Search)
- Independent deployment
- Technology diversity (Python untuk backend, Vue untuk frontend)
- Better fault isolation
- Easier maintenance

---

## PERMASALAHAN 3: Sinkronisasi Data

### Deskripsi
Ketika data berubah di MongoDB, Elasticsearch perlu diperbarui. Bagaimana cara menjaga konsistensi data antar dua database yang berbeda?

### Dampak
- Data di MongoDB dan Elasticsearch bisa tidak sinkron
- User melihat hasil search yang outdated
- Data ghost di Elasticsearch setelah delete dari MongoDB

### Solusi
Implementasi real-time synchronization:
- **CREATE**: Setelah insert ke MongoDB, langsung sync ke Elasticsearch
- **UPDATE**: Setelah update di MongoDB, langsung update di Elasticsearch
- **DELETE**: Setelah delete dari MongoDB, langsung delete dari Elasticsearch

### Implementasi
```python
# Core Service melakukan sync setelah setiap operasi CRUD
async def create_product(product: ProductCreateSchema):
    # 1. Insert ke MongoDB
    produk_dict = product.model_dump(by_alias=True)
    result = mongo.insert_satu(produk_dict)
    
    # 2. Sync ke Search Service
    await sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
    
    return result
```

---

## PERMASALAHAN 4: Environment Consistency

### Deskripsi
Setiap developer dan production environment memiliki konfigurasi yang berbeda (Python version, library versions, port configurations, dll).

### Dampak
- "It works on my machine" syndrome
- Deployment errors
- Inconsistent behavior antar environment
- Time wasted debugging environment issues

### Solusi
Menggunakan Docker untuk containerization:
- **Docker Image**: Standardized environment
- **Docker Compose**: Multi-container orchestration
- **Health Checks**: Pastikan semua service ready sebelum dijalankan
- **Volumes**: Data persistence untuk MongoDB dan Elasticsearch

### Implementasi
```yaml
# docker-compose.yml
services:
  mongodb:
    image: mongo:7
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
    
  elasticsearch:
    image: elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
```

---

## PERMASALAHAN 5: Pydantic v2 Compatibility

### Deskripsi
Project awalnya menggunakan Pydantic v1, tetapi environment menggunakan Pydantic v2 yang memiliki breaking changes, terutama pada field naming dengan leading underscore.

### Dampak
- `NameError: Fields must not use names with leading underscores`
- Schema validation gagal
- API tidak bisa berjalan

### Solusi
Mengadopsi Pydantic v2 patterns:
- **Field Alias**: Menggunakan `id` sebagai field name dengan `alias="_id"`
- **Config**: Menambahkan `from_attributes = True` dan `populate_by_name = True`
- **model_dump()**: Menggunakan `by_alias=True` untuk serialisasi

### Implementasi
```python
class ProductSchema(BaseModel):
    id: int = Field(..., alias="_id")  # Python: product.id, JSON: "_id"
    nama: str
    harga: int
    
    class Config:
        populate_by_name = True
        from_attributes = True

# Usage
product = ProductSchema(id=1, nama="Laptop", harga=5000000)
print(product.id)  # 1
print(product.model_dump(by_alias=True))  # {"_id": 1, "nama": "Laptop", ...}
```

---

## PERMASALAHAN 6: Elasticsearch _id Field Conflict

### Deskripsi
Elasticsearch memperlakukan `_id` sebagai metadata field, bukan field yang disimpan di `_source`. Ketika mencoba mengirim `_id` di document body, Elasticsearch menolak dengan error.

### Dampak
- `RequestError: Field [_id] is a metadata field and cannot be added inside a document`
- Indexing gagal
- Data tidak masuk ke Elasticsearch

### Solusi
Memisahkan document ID dari document body:
- **ID**: Dikirim sebagai parameter `id` di Elasticsearch client
- **Body**: Hanya berisi field-field lain tanpa `_id`

### Implementasi
```python
# SEBELUM (SALAH)
client.index(
    index=ELASTIC_INDEX_NAME,
    id=doc_id,
    body=data  # ❌ Contains _id
)

# SESUDAH (BENAR)
doc_body = {k: v for k, v in data.items() if k != "_id"}
client.index(
    index=ELASTIC_INDEX_NAME,
    id=doc_id,  # ✅ ID sebagai parameter
    body=doc_body  # ✅ Body tanpa _id
)
```

---

## PERMASALAHAN 7: Bulk Sync Menghapus Seluruh Data

### Deskripsi
Endpoint `/api/sync` untuk bulk sync menggunakan `index_banyak()` yang menghapus seluruh index sebelum mengindex data baru. Ketika digunakan untuk sync single product, semua data lama hilang.

### Dampak
- Setelah create 1 produk, semua produk lain hilang dari Elasticsearch
- Search hanya menampilkan produk terbaru
- Data loss di search index

### Solusi
Membuat endpoint terpisah untuk single product sync:
- **POST /api/sync**: Bulk sync (untuk seed data) - tetap menghapus index
- **POST /api/sync/single**: Single product sync - tanpa menghapus index

### Implementasi
```python
# Core Service
# CREATE product menggunakan endpoint single
await sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)

# SEED data menggunakan endpoint bulk
await sinkronisasi_ke_search_service("POST", "/sync", {"products": data})
```

---

## RINGKASAN SOLUSI

| Permasalahan | Akar Penyebab | Solusi | Hasil |
|-------------|---------------|--------|-------|
| Pencarian lambat | Regex MongoDB | Elasticsearch | 10-100x lebih cepat |
| Monolith | Semua dalam satu app | Microservices | Scalable & maintainable |
| Sinkronisasi data | 2 database berbeda | Real-time sync hook | Data konsisten |
| Environment inconsistency | Manual setup | Docker | Consistent environment |
| Pydantic v2 | Breaking changes | Field alias pattern | Compatible |
| ES _id conflict | Metadata field | Separate ID & body | No error |
| Bulk sync issue | Delete all index | Separate endpoint | Data aman |

---

## LESSONS LEARNED

1. **Technology Selection**: Memilih teknologi yang tepat untuk use case yang tepat (MongoDB untuk CRUD, ES untuk Search)
2. **Architecture**: Microservices memungkinkan scalability dan maintainability yang lebih baik
3. **Data Consistency**: Sinkronisasi real-time penting untuk menjaga konsistensi antar database
4. **Modern Python**: Pydantic v2 memiliki breaking changes, perlu adaptasi
5. **Elasticsearch**: Memahami konsep dasar ES (index, mapping, metadata field) sangat penting
6. **Containerization**: Docker memudahkan deployment dan konsistensi environment