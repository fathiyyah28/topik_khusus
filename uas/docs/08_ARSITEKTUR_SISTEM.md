# ARSITEKTUR SISTEM

## Overview
Bagian ini menjelaskan arsitektur keseluruhan sistem, komponen-komponen yang terlibat, dan bagaimana mereka berinteraksi satu sama lain.

---

## High-Level Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Vue.js 3 + Bootstrap 5 + Axios                         │ │
│  │  Port: 3000                                              │ │
│  │  - User Interface                                        │ │
│  │  - Product Management                                    │ │
│  │  - Search Interface                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API (JSON)
                            │
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND LAYER                               │
│                                                                  │
│  ┌────────────────────────┐  ┌──────────────────────────────┐  │
│  │   Core Service         │  │   Search Service              │  │
│  │   (FastAPI)            │  │   (FastAPI)                   │  │
│  │   Port: 8001           │  │   Port: 8002                  │  │
│  │                        │  │                               │  │
│  │  Responsibilities:     │  │  Responsibilities:            │  │
│  │  - Create Product      │  │  - Full-text Search           │  │
│  │  - Read Products       │  │  - Index Management           │  │
│  │  - Update Product      │  │  - Relevance Scoring          │  │
│  │  - Delete Product      │  │  - Sync from Core             │  │
│  │  - MongoDB CRUD        │  │  - Elasticsearch Operations   │  │
│  │  - Sync to Search      │  │                               │  │
│  └───────────┬────────────┘  └───────────────┬───────────────┘  │
│              │                                │                  │
│              │ HTTP Sync                      │                  │
│              │                                │                  │
└──────────────┼────────────────────────────────┼──────────────────┘
               │                                │
               ▼                                ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│   DATABASE LAYER         │      │   SEARCH ENGINE LAYER    │
│                          │      │                          │
│  ┌────────────────────┐  │      │  ┌────────────────────┐  │
│  │   MongoDB          │  │      │  │  Elasticsearch     │  │
│  │   Port: 27017      │  │      │  │  Port: 9200        │  │
│  │                    │  │      │  │                    │  │
│  │  - Primary Store   │  │      │  │  - Full-text Index │  │
│  │  - Document Store  │  │      │  │  - Inverted Index  │  │
│  │  - CRUD Operations │  │      │  │  - Search Engine   │  │
│  │  - Data Source     │  │      │  │  - Relevance Score │  │
│  │                    │  │      │  │                    │  │
│  │  Database: uas_db  │  │      │  │  Index: produk     │  │
│  │  Collection:       │  │      │  │                    │  │
│  │  products          │  │      │  │                    │  │
│  └────────────────────┘  │      │  └────────────────────┘  │
└──────────────────────────┘      └──────────────────────────┘
               │                                │
               └────────────────┬───────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   DOCKER LAYER         │
                    │                        │
                    │  ┌──────────────────┐  │
                    │  │ Docker Compose   │  │
                    │  │                  │  │
                    │  │ - Containerization│  │
                    │  │ - Orchestration  │  │
                    │  │ - Networking     │  │
                    │  │ - Volumes        │  │
                    │  └──────────────────┘  │
                    │                        │
                    │  Network: uas_app-network│
                    │  (Bridge Network)       │
                    └────────────────────────┘
```

---

## Detailed Component Architecture

### 1. Frontend Layer

#### Technology Stack
- **Vue.js 3**: Progressive JavaScript framework
- **Bootstrap 5**: CSS framework untuk styling
- **Axios**: HTTP client untuk API calls

#### Responsibilities
- User interface untuk product management
- Form handling untuk CRUD operations
- Search interface dengan real-time results
- Display product list dengan pagination
- Responsive design untuk mobile dan desktop

#### Components Structure
```
frontend/src/
├── components/
│   ├── ProductList.vue          # Display all products
│   ├── ProductForm.vue          # Create/Edit product form
│   ├── ProductCard.vue          # Single product display
│   ├── SearchBar.vue            # Search input component
│   └── SearchResults.vue        # Display search results
├── services/
│   └── api.js                   # Axios configuration
├── App.vue                      # Main application
└── main.js                      # Entry point
```

#### API Communication
```javascript
// services/api.js
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001/api'

export default {
  // Products
  async getAllProducts() {
    const response = await axios.get(`${API_BASE_URL}/products`)
    return response.data
  },
  
  async getProduct(id) {
    const response = await axios.get(`${API_BASE_URL}/products/${id}`)
    return response.data
  },
  
  async createProduct(product) {
    const response = await axios.post(`${API_BASE_URL}/products`, product)
    return response.data
  },
  
  async updateProduct(id, product) {
    const response = await axios.put(`${API_BASE_URL}/products/${id}`, product)
    return response.data
  },
  
  async deleteProduct(id) {
    const response = await axios.delete(`${API_BASE_URL}/products/${id}`)
    return response.data
  },
  
  // Search
  async searchProducts(query) {
    const response = await axios.get(`http://localhost:8002/api/search?q=${query}`)
    return response.data
  }
}
```

---

### 2. Core Service Layer

#### Technology Stack
- **FastAPI**: Modern Python web framework
- **Pydantic v2**: Data validation dan serialization
- **httpx**: Async HTTP client untuk sync
- **PyMongo**: MongoDB driver

#### Architecture
```
core-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── routes.py            # API endpoints
│   ├── schemas.py           # Pydantic models
│   ├── mongo_service.py     # MongoDB operations
│   └── config.py            # Configuration
├── Dockerfile
└── requirements.txt
```

#### main.py
```python
from fastapi import FastAPI
from app.routes import router as product_router

app = FastAPI(
    title="Core Service API",
    description="Product Management Service",
    version="1.0.0"
)

# Include routers
app.include_router(product_router, prefix="/api", tags=["products"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "core-service"}
```

#### routes.py Structure
```python
from fastapi import APIRouter, HTTPException
from app import mongo_service as mongo
from app.schemas import ProductCreateSchema, ProductUpdateSchema

router = APIRouter()

# CRUD Endpoints
@router.get("/products")                    # Read all
@router.get("/products/{product_id}")       # Read one
@router.post("/products")                   # Create
@router.put("/products/{product_id}")       # Update
@router.delete("/products/{product_id}")    # Delete
@router.post("/products/seed")              # Bulk import

# Sync Function
async def sinkronisasi_ke_search_service(method, endpoint, data):
    # HTTP call to Search Service
    pass
```

#### schemas.py Structure
```python
from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    id: int = Field(..., alias="_id")
    nama: str
    kategori: str
    harga: int = Field(..., ge=0)
    stok: int = Field(..., ge=0)
    spesifikasi: str
    
    class Config:
        populate_by_name = True
        from_attributes = True

class ProductUpdateSchema(BaseModel):
    nama: Optional[str] = None
    kategori: Optional[str] = None
    harga: Optional[int] = None
    stok: Optional[int] = None
    spesifikasi: Optional[str] = None
```

#### Data Flow
```
Request Flow:
1. Client sends HTTP request
2. FastAPI receives dan validates with Pydantic
3. Route handler processes request
4. MongoDB service executes CRUD
5. Sync to Search Service (async)
6. Return response to client

Example: Create Product
POST /api/products
    ↓
Validate with ProductCreateSchema
    ↓
Insert to MongoDB
    ↓
Sync to Search Service (POST /api/sync/single)
    ↓
Return ProductResponse
```

---

### 3. Search Service Layer

#### Technology Stack
- **FastAPI**: Web framework
- **Elasticsearch Client**: ES interaction
- **Pydantic v2**: Request/Response validation

#### Architecture
```
search-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── routes.py            # API endpoints
│   ├── elastic_service.py   # Elasticsearch operations
│   └── schemas.py           # Pydantic models
├── Dockerfile
└── requirements.txt
```

#### main.py
```python
from fastapi import FastAPI
from app.routes import router as search_router

app = FastAPI(
    title="Search Service API",
    description="Elasticsearch Search Service",
    version="1.0.0"
)

app.include_router(search_router, prefix="/api", tags=["search"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "search-service"}
```

#### routes.py Structure
```python
from fastapi import APIRouter, HTTPException
from app import elastic_service as es

router = APIRouter()

# Search Endpoints
@router.get("/search")                    # Full-text search
@router.get("/stats")                     # Index statistics

# Sync Endpoints (called by Core Service)
@router.post("/sync")                     # Bulk sync (seed)
@router.post("/sync/single")              # Single product sync
@router.put("/sync/{product_id}")         # Update product
@router.delete("/sync/{product_id}")      # Delete product
```

#### elastic_service.py Structure
```python
from elasticsearch import Elasticsearch

# Connection
def dapatkan_koneksi():
    # Create ES client
    pass

# Index Management
def buat_index():
    # Create index with mapping
    pass

# CRUD Operations
def index_satu(produk):
    # Index single document
    pass

def index_banyak(data_list):
    # Bulk index documents
    pass

def update_data(produk_id, data_baru):
    # Update document
    pass

def delete_data(produk_id):
    # Delete document
    pass

# Search
def cari_match(keyword):
    # Full-text search
    pass
```

#### Data Flow
```
Sync Flow (from Core Service):
1. Core Service sends HTTP POST/PUT/DELETE
2. FastAPI receives request
3. Elasticsearch service executes operation
4. Return success/error response

Search Flow:
1. User sends search query
2. FastAPI receives query parameter
3. Elasticsearch service executes search
4. ES returns results with scores
5. Format dan return to client

Example: Search
GET /api/search?q=laptop
    ↓
Analyze query: "laptop" → ["laptop"]
    ↓
Search in Elasticsearch
    ↓
Return top N results with scores
```

---

### 4. Database Layer

#### MongoDB (Primary Database)

**Purpose**: Primary data storage untuk semua products

**Schema**:
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

**Connection**:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017")
db = client["uas_db"]
collection = db["products"]
```

**Operations**:
- insert_one() / insert_many()
- find() / find_one()
- update_one() / update_many()
- delete_one() / delete_many()

#### Elasticsearch (Search Engine)

**Purpose**: Full-text search dan indexing untuk fast search

**Index Mapping**:
```json
{
  "mappings": {
    "properties": {
      "nama": {"type": "text", "analyzer": "standard"},
      "kategori": {"type": "text", "analyzer": "standard"},
      "harga": {"type": "integer"},
      "stok": {"type": "integer"},
      "spesifikasi": {"type": "text", "analyzer": "standard"}
    }
  }
}
```

**Connection**:
```python
from elasticsearch import Elasticsearch

client = Elasticsearch("http://elasticsearch:9200")
```

**Operations**:
- index() - Create/Update document
- search() - Full-text search
- update() - Partial update
- delete() - Delete document

---

### 5. Docker Layer

#### Container Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host                               │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Docker Compose Network: uas_app-network              │ │
│  │  (Bridge Network - 172.20.0.0/16)                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ core-service │  │search-service│  │   frontend   │    │
│  │  Container   │  │  Container   │  │   Container  │    │
│  │              │  │              │  │              │    │
│  │ IP: 172.20.0.2│  │ IP: 172.20.0.3│  │ IP: 172.20.0.4│  │
│  │ Port: 8001   │  │ Port: 8002   │  │ Port: 3000   │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                  │                  │             │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐    │
│  │   MongoDB    │  │ Elasticsearch│  │              │    │
│  │  Container   │  │  Container   │  │              │    │
│  │              │  │              │  │              │    │
│  │ IP: 172.20.0.5│  │ IP: 172.20.0.6│  │              │    │
│  │ Port: 27017  │  │ Port: 9200   │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  Volumes:                                                   │
│  - mongodb_data (/var/lib/docker/volumes/)                 │
│  - elasticsearch_data (/var/lib/docker/volumes/)           │
└─────────────────────────────────────────────────────────────┘
```

#### Network Communication
```
Service Discovery via Docker DNS:

Core Service → Search Service:
  URL: http://search-service:8002
  Resolved: 172.20.0.3:8002

Core Service → MongoDB:
  URL: http://mongodb:27017
  Resolved: 172.20.0.5:27017

Search Service → Elasticsearch:
  URL: http://elasticsearch:9200
  Resolved: 172.20.0.6:9200
```

---

## Communication Patterns

### 1. Synchronous Communication (Request/Response)

**Core Service → MongoDB**:
```python
# Direct database call
product = collection.find_one({"_id": product_id})
```

**Frontend → Core Service**:
```javascript
// HTTP GET request
const response = await axios.get('/api/products')
```

**Core Service → Search Service**:
```python
# HTTP POST for sync
async with httpx.AsyncClient() as client:
    await client.post(
        "http://search-service:8002/api/sync/single",
        json=product_data
    )
```

### 2. Asynchronous Communication (Fire-and-Forget)

**Core Service → Search Service (Async Sync)**:
```python
# Create background task
asyncio.create_task(
    sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
)

# Immediately return response to client
# Sync happens in background
```

**Benefit**: Client tidak perlu tunggu sync selesai

### 3. Data Flow Patterns

#### Pattern 1: Request-Response (Synchronous)
```
Client          Core Service      MongoDB
  │                │                │
  │──GET /products─>│                │
  │                │──find()────────>│
  │                │<──[products]────│
  │<──[products]────│                │
  │                │                │
```

#### Pattern 2: Fire-and-Forget (Asynchronous)
```
Client          Core Service      Search Service     Elasticsearch
  │                │                │                  │
  │──POST /product─>│                │                  │
  │                │──insert()──────>│                  │
  │                │<──[success]─────│                  │
  │                │                │                  │
  │                │──POST /sync────┼──────────────────>│
  │<──[success]────│                │                  │
  │                │                │──index()─────────>│
  │                │                │<──[indexed]───────│
```

#### Pattern 3: Pipeline (CRUD + Search)
```
CREATE Product:
1. Client → Core: POST /api/products
2. Core → MongoDB: insert_one()
3. Core → Search: POST /api/sync/single
4. Search → Elasticsearch: index()
5. Core → Client: Return product

UPDATE Product:
1. Client → Core: PUT /api/products/1
2. Core → MongoDB: update_one()
3. Core → Search: PUT /api/sync/1
4. Search → Elasticsearch: update()
5. Core → Client: Return updated product

DELETE Product:
1. Client → Core: DELETE /api/products/1
2. Core → MongoDB: delete_one()
3. Core → Search: DELETE /api/sync/1
4. Search → Elasticsearch: delete()
5. Core → Client: Return success
```

---

## Security Architecture

### 1. Network Security
```
┌─────────────────────────────────────────┐
│  Docker Network (uas_app-network)       │
│                                         │
│  - Isolated from external network       │
│  - Internal DNS resolution              │
│  - No direct external access            │
│                                         │
│  Only exposed ports:                    │
│  - 3000 (Frontend)                      │
│  - 8001 (Core Service)                  │
│  - 8002 (Search Service)                │
│  - 27017 (MongoDB) - optional           │
│  - 9200 (Elasticsearch) - optional      │
└─────────────────────────────────────────┘
```

### 2. Application Security
- **Input Validation**: Pydantic schemas validate all inputs
- **Type Safety**: Type hints prevent injection attacks
- **Error Handling**: No sensitive data in error messages
- **Health Checks**: Separate endpoint untuk monitoring

### 3. Data Security
- **No SQL Injection**: Using parameterized queries (PyMongo)
- **No XSS**: Vue.js auto-escapes output
- **CORS**: Can be configured di FastAPI
- **Secrets Management**: Environment variables untuk credentials

---

## Scalability Architecture

### Horizontal Scaling

#### Core Service Scaling
```
Load Balancer
     │
     ├─> Core Service Instance 1
     ├─> Core Service Instance 2
     ├─> Core Service Instance 3
     └─> Core Service Instance N

Each instance:
- Shares same MongoDB
- Independent scaling
- Stateless (no local storage)
```

#### Search Service Scaling
```
Load Balancer
     │
     ├─> Search Service Instance 1
     ├─> Search Service Instance 2
     └─> Search Service Instance N

Each instance:
- Shares same Elasticsearch cluster
- Independent scaling
- Stateless (no local storage)
```

### Database Scaling

#### MongoDB Scaling
```
Primary Node (Read/Write)
    │
    ├─> Secondary Node 1 (Read)
    ├─> Secondary Node 2 (Read)
    └─> Secondary Node 3 (Read)

Replication:
- Automatic failover
- Read scaling (read from secondaries)
- Write scaling (sharding)
```

#### Elasticsearch Scaling
```
Master Node
    │
    ├─> Data Node 1 (Shard 0, 1, 2)
    ├─> Data Node 2 (Shard 3, 4, 5)
    └─> Data Node 3 (Shard 6, 7, 8)

Each shard:
- Primary shard (read/write)
- Replica shard (read only)
- Distributed across nodes
```

---

## Monitoring & Observability

### 1. Logging
```python
import logging

logger = logging.getLogger(__name__)

# Structured logging
logger.info(f"Product created: {product_id}")
logger.error(f"Failed to sync: {error}")
```

### 2. Metrics
```python
# Request metrics
- Request count
- Response time
- Error rate
- Active connections

# Business metrics
- Products created/hour
- Search queries/second
- Sync success rate
```

### 3. Health Checks
```python
# Core Service
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mongodb": mongo.cek_koneksi(),
        "search_service": await check_search_service()
    }

# Search Service
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "elasticsearch": es.cek_koneksi()
    }
```

---

## Deployment Architecture

### Development
```
Developer Machine
    │
    ├─> Docker Desktop
    │   ├─> Core Service (localhost:8001)
    │   ├─> Search Service (localhost:8002)
    │   ├─> MongoDB (localhost:27017)
    │   ├─> Elasticsearch (localhost:9200)
    │   └─> Frontend (localhost:3000)
    │
    └─> Hot reload enabled
        - Code changes auto-reload
        - Volume mounts for development
```

### Production
```
Load Balancer (Nginx)
    │
    ├─> Core Service Cluster (3 instances)
    │   ├─> Instance 1
    │   ├─> Instance 2
    │   └─> Instance 3
    │
    ├─> Search Service Cluster (2 instances)
    │   ├─> Instance 1
    │   └─> Instance 2
    │
    ├─> MongoDB Replica Set (3 nodes)
    │   ├─> Primary
    │   ├─> Secondary 1
    │   └─> Secondary 2
    │
    └─> Elasticsearch Cluster (3 nodes)
        ├─> Master + Data Node 1
        ├─> Data Node 2
        └─> Data Node 3
```

---

## Technology Decisions

### Why This Architecture?

1. **Microservices**: Separation of concerns, independent scaling
2. **MongoDB**: Flexible schema, JSON-like, perfect untuk CRUD
3. **Elasticsearch**: Fast full-text search, relevance scoring
4. **FastAPI**: High performance, async support, auto documentation
5. **Vue.js**: Easy to learn, reactive, good documentation
6. **Docker**: Consistency, portability, easy deployment

### Trade-offs

**Pros**:
✅ Scalable dan maintainable
✅ Technology diversity
✅ Independent deployment
✅ Fault isolation
✅ Modern tech stack

**Cons**:
❌ Operational complexity
❌ Network latency
❌ Distributed system challenges
❌ More infrastructure needed
❌ Learning curve

---

## Future Enhancements

### Potential Additions
1. **API Gateway**: Nginx/Kong untuk routing dan auth
2. **Message Queue**: RabbitMQ/Kafka untuk async communication
3. **Cache Layer**: Redis untuk frequent queries
4. **Authentication**: JWT/OAuth2 untuk user authentication
5. **Monitoring**: Prometheus + Grafana untuk metrics
6. **Logging**: ELK Stack untuk centralized logging
7. **CI/CD**: GitHub Actions/GitLab CI untuk automation
8. **Load Balancer**: Nginx/HAProxy untuk traffic distribution
9. **Service Mesh**: Istio untuk service-to-service communication
10. **Analytics**: Dedicated analytics service untuk business insights