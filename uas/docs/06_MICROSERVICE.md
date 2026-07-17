# MICROSERVICES

## Apa itu Microservices?

### Definisi
Microservices adalah arsitektur software development di mana aplikasi dibangun sebagai kumpulan small, independent, loosely-coupled services yang berkomunikasi melalui well-defined APIs (biasanya HTTP/REST). Setiap service menangani specific business capability dan bisa di-deploy, scaled, dan maintained secara independen.

### Karakteristik Utama

1. **Single Responsibility**: Setiap service fokus pada satu business capability
2. **Independently Deployable**: Bisa di-deploy tanpa affect services lain
3. **Decentralized**: Setiap service bisa menggunakan technology stack yang berbeda
4. **Failure Isolation**: Failure di satu service tidak affect services lain
5. **Scalable**: Bisa di-scale secara independen berdasarkan kebutuhan

---

## Monolith vs Microservices

### Monolith Architecture

#### Struktur
```
┌─────────────────────────────────────────────┐
│         MONOLITH APPLICATION                │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │  User Interface Layer                 │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  Business Logic Layer                 │  │
│  │  - CRUD Operations                    │  │
│  │  - Search Operations                  │  │
│  │  - Authentication                     │  │
│  │  - Authorization                      │  │
│  │  - Validation                         │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  Data Access Layer                    │  │
│  │  - Database Connections               │  │
│  │  - ORM                                 │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │  Single Database                      │  │
│  │  - users table                        │  │
│  │  - products table                     │  │
│  │  - orders table                       │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

#### Code Example (Monolith)
```python
# app.py - Everything in one file
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# CRUD Module
@app.post("/products")
def create_product(product: Product):
    db.insert(product)
    return product

@app.get("/products")
def get_products():
    return db.find_all()

# Search Module
@app.get("/search")
def search_products(q: str):
    results = db.regex_search(q)  # Slow!
    return results

# Auth Module
@app.post("/login")
def login(username: str, password: str):
    user = db.find_user(username)
    if verify_password(password, user.password):
        return create_token(user)
    raise HTTPException(401)

# Business Logic
@app.post("/orders")
def create_order(order: Order):
    product = db.find_product(order.product_id)
    if product.stok < order.qty:
        raise HTTPException(400, "Insufficient stock")
    db.insert(order)
    db.update_stock(order.product_id, -order.qty)
    return order
```

### Microservices Architecture

#### Struktur
```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Client    │      │    Client    │      │    Client    │
│  (Browser)   │      │  (Mobile)    │      │   (API)      │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Gateway     │
                    │  (Load Balancer)  │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Core Service │      │Search Service│      │ Auth Service │
│  (CRUD)      │      │  (Search)    │      │  (Login)     │
│  :8001       │      │  :8002       │      │  :8003       │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   MongoDB    │      │ Elasticsearch│      │  PostgreSQL  │
│   :27017     │      │   :9200      │      │   :5432      │
└──────────────┘      └──────────────┘      └──────────────┘
```

#### Code Example (Microservices)

**Core Service** (`core-service/app/routes.py`):
```python
# CRUD operations only
@router.post("/products")
async def create_product(product: ProductCreateSchema):
    # 1. Insert to MongoDB
    produk_dict = product.model_dump(by_alias=True)
    result = mongo.insert_satu(produk_dict)
    
    # 2. Sync to Search Service (async, fire-and-forget)
    asyncio.create_task(
        sinkronisasi_ke_search_service("POST", "/sync/single", produk_dict)
    )
    
    return result

@router.get("/products")
async def get_products():
    return mongo.cari_semua()

@router.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdateSchema):
    data_baru = product.model_dump(exclude_none=True, by_alias=True)
    mongo.update_data(product_id, data_baru)
    
    # Sync to Search Service
    asyncio.create_task(
        sinkronisasi_ke_search_service("PUT", f"/sync/{product_id}", data_baru)
    )
    
    return mongo.cari_by_id(product_id)
```

**Search Service** (`search-service/app/routes.py`):
```python
# Search operations only
@router.get("/search")
async def search_products(q: str):
    hasil = es.cari_match(q)
    return {"data": hasil, "total": len(hasil)}

@router.post("/sync/single")
async def sync_single_product(product: Dict[str, Any]):
    es.index_satu(product)
    return {"status": "success"}

@router.put("/sync/{product_id}")
async def sync_update_product(product_id: int, data: Dict[str, Any]):
    es.update_data(product_id, data)
    return {"status": "success"}
```

---

## Perbandingan Detail

### 1. Development

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Codebase** | Single codebase | Multiple codebases |
| **Setup** | Simple (one project) | Complex (multiple projects) |
| **Debugging** | Easy (single process) | Hard (distributed tracing needed) |
| **Testing** | Simple integration tests | Complex (need contract testing) |
| **IDE** | Single IDE workspace | Multiple IDE windows |
| **Version Control** | Single repo | Multiple repos atau monorepo |

### 2. Deployment

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Deployment** | Deploy entire app | Deploy individual services |
| **Downtime** | Full app downtime | Only affected service down |
| **Rollback** | Rollback entire app | Rollback specific service |
| **CI/CD** | Single pipeline | Multiple pipelines |
| **Release Frequency** | Slower (coordinate releases) | Faster (independent releases) |
| **Risk** | High (all or nothing) | Low (gradual rollout) |

### 3. Scalability

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Scaling** | Scale entire app | Scale specific services |
| **Resource Usage** | Wasteful (scale unused parts) | Efficient (scale what's needed) |
| **Cost** | Higher (over-provisioning) | Lower (right-sizing) |
| **Performance** | Better (no network overhead) | Good (network calls add latency) |
| **Load Distribution** | Uneven | Even (per-service) |

**Example Scenario:**
```
Scenario: 1000 concurrent users
- 800 doing CRUD operations
- 200 doing search operations

Monolith:
  - Need to scale entire app to handle 1000 users
  - Waste resources on search scaling if that's not the bottleneck

Microservices:
  - Scale Core Service to 8 instances (handle 800 users)
  - Scale Search Service to 2 instances (handle 200 users)
  - Optimal resource usage
```

### 4. Technology

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Tech Stack** | Single technology | Polyglot (different per service) |
| **Flexibility** | Locked to one stack | Freedom to choose best tool per service |
| **Upgrades** | Hard (affects entire app) | Easy (upgrade one service) |
| **Innovation** | Slow (legacy code holds back) | Fast (new services use modern tech) |

**Example:**
```
Monolith:
  - Built with Flask (Python)
  - Need better performance? Must rewrite entire app

Microservices:
  - Core Service: FastAPI (Python) - high performance CRUD
  - Search Service: FastAPI + Elasticsearch - optimized search
  - Auth Service: Node.js - real-time features
  - Analytics Service: Go - high throughput
```

### 5. Team Organization

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Team Structure** | Centralized team | Cross-functional teams |
| **Ownership** | Shared ownership | Clear ownership per service |
| **Communication** | High (everyone talks) | Low (service boundaries) |
| **Autonomy** | Low (coordinate changes) | High (independent work) |
| **Conway's Law** | System mirrors org structure | Services map to teams |

**Example:**
```
Monolith (10 developers):
  - Everyone works on same codebase
  - Merge conflicts frequent
  - Hard to parallelize work

Microservices (10 developers):
  - Team A (3 devs): Core Service
  - Team B (3 devs): Search Service
  - Team C (2 devs): Frontend
  - Team D (2 devs): Infrastructure
  - Minimal conflicts, parallel development
```

### 6. Fault Isolation

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Failure Impact** | Entire app down | Only affected service down |
| **Resilience** | Low (single point of failure) | High (circuit breakers, fallbacks) |
| **Monitoring** | Simple (one app) | Complex (distributed tracing) |
| **Recovery** | Slow (restart entire app) | Fast (restart specific service) |

**Example:**
```
Scenario: Search Service crashes

Monolith:
  - Entire application down
  - Users cannot do CRUD or search
  - Revenue loss

Microservices:
  - Search Service down
  - Core Service still running (CRUD works)
  - Users can still manage products
  - Search shows "temporarily unavailable"
  - Partial functionality preserved
```

### 7. Data Management

| Aspek | Monolith | Microservices |
|-------|----------|---------------|
| **Database** | Single shared database | Database per service |
| **Transactions** | ACID transactions easy | Distributed transactions hard |
| **Consistency** | Strong consistency | Eventual consistency |
| **Schema Changes** | Easy (single DB) | Hard (coordinate migrations) |
| **Data Duplication** | Minimal | Common (denormalization) |

---

## Kelebihan Microservices

✅ **Independent Scaling**: Scale service yang butuh, tidak yang tidak  
✅ **Independent Deployment**: Deploy tanpa affect services lain  
✅ **Technology Diversity**: Pilih tech terbaik per service  
✅ **Fault Isolation**: Failure ter-isolasi per service  
✅ **Team Autonomy**: Tim bisa bekerja independently  
✅ **Easier Maintenance**: Codebase kecil lebih mudah maintain  
✅ **Faster Development**: Tim bisa kerja parallel  
✅ **Better Organization**: Services map to business capabilities  
✅ **Gradual Migration**: Bisa migrate dari monolith gradually  
✅ **Resilience**: Circuit breakers, fallbacks, retries  

---

## Kekurangan Microservices

❌ **Operational Complexity**: Perlu orchestration, monitoring, logging  
❌ **Network Latency**: HTTP calls antar services  
❌ **Distributed System Challenges**: Consistency, transactions, debugging  
❌ **Testing Complexity**: Integration tests lebih sulit  
❌ **More Infrastructure**: Service discovery, load balancers, API gateways  
❌ **Data Consistency**: Eventual consistency lebih kompleks  
❌ **Learning Curve**: Tim perlu learn distributed systems  
❌ **Initial Setup Cost**: Lebih lama setup dibanding monolith  
❌ **Debugging Difficulty**: Need distributed tracing (Jaeger, Zipkin)  
❌ **Security**: More attack surfaces  

---

## Mengapa Project Menggunakan Microservices?

### 1. **Separation of Concerns**

**Core Service** (Port 8001):
- **Responsibility**: CRUD operations
- **Database**: MongoDB
- **Technology**: FastAPI + PyMongo
- **Team**: Backend team focused on data operations

**Search Service** (Port 8002):
- **Responsibility**: Full-text search
- **Database**: Elasticsearch
- **Technology**: FastAPI + Elasticsearch client
- **Team**: Backend team focused on search

**Benefit**: Setiap service memiliki clear responsibility, mudah di-understand dan di-maintain.

### 2. **Independent Scaling**

```
Scenario: Black Friday sale
- CRUD operations: 1000 req/s
- Search operations: 5000 req/s

Solution:
- Core Service: Scale to 5 instances
- Search Service: Scale to 20 instances
- Frontend: Scale to 10 instances

Without microservices:
- Must scale entire monolith to handle 5000 req/s
- Waste resources on CRUD scaling
```

### 3. **Technology Optimization**

```
Core Service:
- Python/FastAPI: Optimal untuk I/O-bound CRUD operations
- MongoDB: Document database untuk flexible schema
- PyMongo: Async driver untuk high performance

Search Service:
- Python/FastAPI: Consistent dengan Core Service
- Elasticsearch Client: Native ES integration
- Specialized untuk text search operations

Frontend:
- Vue.js 3: Reactive UI, easy to learn
- Bootstrap 5: Rapid UI development
- Axios: HTTP client untuk API calls
```

### 4. **Fault Isolation**

```
Scenario: Elasticsearch crashes

Impact:
- Search Service: Returns error "Search unavailable"
- Core Service: Still running (CRUD works)
- Frontend: Shows "Search temporarily unavailable" message
- Users: Can still manage products, just can't search

Without microservices (monolith):
- Entire application crashes
- Users cannot do anything
- Complete service outage
```

### 5. **Team Collaboration**

```
Team Structure:
- Frontend Team (2 devs): Vue.js, Bootstrap
  - Responsible: UI/UX, user interactions
  
- Core Service Team (2 devs): FastAPI, MongoDB
  - Responsible: CRUD operations, data management
  
- Search Service Team (2 devs): FastAPI, Elasticsearch
  - Responsible: Search functionality, indexing
  
- DevOps (1 dev): Docker, deployment, monitoring

Benefit:
- Clear ownership
- Minimal conflicts
- Parallel development
- Specialization
```

### 6. **Easier Testing**

```
Unit Testing:
- Test Core Service independently
- Test Search Service independently
- Mock dependencies

Integration Testing:
- Test Core Service → MongoDB
- Test Search Service → Elasticsearch
- Test Core Service → Search Service (contract testing)

Without microservices:
- Must test entire application together
- Slower test execution
- Harder to isolate failures
```

### 7. **Future-Proofing**

```
Easy to add new services:
- Recommendation Service (machine learning)
- Notification Service (email, push)
- Analytics Service (data analytics)
- Payment Service (payment gateway)

Each service:
- Independent development
- Independent deployment
- Independent scaling
- No need to modify existing services
```

---

## Komunikasi Antar Service

### 1. REST API (HTTP)

#### Synchronous Communication
```python
# Core Service → Search Service
import httpx

async def sinkronisasi_ke_search_service(
    method: str,
    endpoint: str,
    data: Dict[str, Any] = None
):
    url = f"http://search-service:8002/api{endpoint}"
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        if method == "POST":
            response = await client.post(url, json=data)
        elif method == "PUT":
            response = await client.put(url, json=data)
        elif method == "DELETE":
            response = await client.delete(url)
    
    return response.status_code
```

#### Request/Response Flow
```
Core Service                    Search Service
     │                                │
     │  POST /api/sync/single         │
     │  {product data}                │
     │───────────────────────────────>│
     │                                │
     │          Index to Elasticsearch│
     │                                │
     │  201 Created                   │
     │  {status: success}             │
     │<───────────────────────────────│
     │                                │
```

### 2. Message Queue (Async - Optional)

Untuk lebih async dan resilient, bisa menggunakan message queue:

```python
# Core Service
import aio_pika

async def publish_sync_event(product: dict):
    connection = await aio_pika.connect_robust("amqp://rabbitmq")
    channel = await connection.channel()
    
    queue = await channel.declare_queue("sync_queue", durable=True)
    
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(product).encode()),
        routing_key="sync_queue"
    )

# Search Service
async def consume_sync_events():
    connection = await aio_pika.connect_robust("amqp://rabbitmq")
    channel = await connection.channel()
    
    queue = await channel.declare_queue("sync_queue", durable=True)
    
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                product = json.loads(message.body)
                es.index_satu(product)
```

**Keuntungan Message Queue:**
✅ Decoupling: Services tidak perlu know each other  
✅ Retry: Automatic retry jika service down  
✅ Load Leveling: Buffer untuk burst traffic  
✅ Async: Core Service tidak blocked  

### 3. Service Discovery

#### Docker Compose (Project Ini)
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

```python
# Core Service mengakses Search Service
url = "http://search-service:8002/api/sync/single"
# Docker DNS resolves "search-service" ke IP address
```

#### Service Registry (Production)
```python
# Consul / etcd / Kubernetes Service
url = "http://search-service.service.consul:8002/api/sync/single"
```

### 4. API Gateway Pattern

```
                    ┌──────────────┐
                    │ API Gateway  │
                    │  (Nginx)     │
                    │  :80/:443    │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Core Service │ │Search Service│ │ Auth Service │
    │   :8001      │ │   :8002      │ │   :8003      │
    └──────────────┘ └──────────────┘ └──────────────┘
```

**Keuntungan API Gateway:**
✅ Single entry point  
✅ Authentication/Authorization centralized  
✅ Rate limiting  
✅ Load balancing  
✅ Request routing  
✅ SSL termination  
✅ Logging dan monitoring  

---

## Diagram Arsitektur Microservices

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │   Mobile     │  │   API Client │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Nginx / Kong / AWS API Gateway                       │ │
│  │  - Routing                                             │ │
│  │  - Authentication                                      │ │
│  │  - Rate Limiting                                       │ │
│  │  - Load Balancing                                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Core Service │   │Search Service│   │ Auth Service │
│  (CRUD)      │   │  (Search)    │   │  (Login)     │
│  FastAPI     │   │  FastAPI     │   │  FastAPI     │
│  :8001       │   │  :8002       │   │  :8003       │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   MongoDB    │   │ Elasticsearch│   │  PostgreSQL  │
│   :27017     │   │   :9200      │   │   :5432      │
└──────────────┘   └──────────────┘   └──────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Docker    │
                    │  Compose    │
                    │  Network    │
                    └─────────────┘
```

### Data Flow Diagram
```
┌──────────┐
│ Frontend │
│  Vue.js  │
└────┬─────┘
     │
     │ 1. HTTP Request: GET /api/products
     ▼
┌──────────────┐
│ Core Service │
│  FastAPI     │
└────┬─────────┘
     │
     │ 2. MongoDB Query: find({})
     ▼
┌──────────────┐
│   MongoDB    │
│  Collection  │
│  products    │
└────┬─────────┘
     │
     │ 3. Return products
     ▼
┌──────────────┐
│ Core Service │
│  Response    │
└────┬─────────┘
     │
     │ 4. HTTP Response: {products: [...]}
     ▼
┌──────────┐
│ Frontend │
│ Display  │
└──────────┘

     │
     │ 5. (Async) Sync to Search Service
     ▼
┌──────────────┐
│Search Service│
│  Elasticsearch│
│  Indexing    │
└──────────────┘
```

---

## Best Practices

### 1. Service Design
✅ Single Responsibility Principle  
✅ Loose Coupling, High Cohesion  
✅ API Versioning  
✅ Backward Compatibility  
✅ Circuit Breaker pattern  
✅ Retry dengan exponential backoff  
✅ Timeout configuration  

### 2. Data Management
✅ Database per service  
✅ Event-driven communication untuk data sync  
✅ CQRS untuk read/write separation  
✅ Eventual consistency accepted  
✅ Saga pattern untuk distributed transactions  

### 3. Communication
✅ Prefer async communication  
✅ Use message queues untuk decoupling  
✅ API Gateway untuk external communication  
✅ Service mesh untuk internal communication (Istio, Linkerd)  

### 4. Monitoring
✅ Distributed tracing (Jaeger, Zipkin)  
✅ Centralized logging (ELK stack)  
✅ Metrics (Prometheus + Grafana)  
✅ Health checks  
✅ Circuit breakers (Hystrix, Resilience4j)  

### 5. Security
✅ API Gateway untuk authentication  
✅ Service-to-service authentication (mTLS, JWT)  
✅ Network segmentation  
✅ Secrets management (Vault, Kubernetes Secrets)  
✅ Rate limiting  

---

## Kapan Menggunakan Microservices?

### ✅ Gunakan Microservices Jika:
- Tim besar (10+ developers)
- Application complex dengan multiple domains
- Need independent scaling
- Different services have different requirements
- Want to use different technologies
- Need high availability
- Have DevOps capability

### ❌ Jangan Gunakan Microservices Jika:
- Tim kecil (1-3 developers)
- Application simple
- Early stage startup (need to move fast)
- Limited DevOps resources
- Strong consistency required
- Performance critical (latency-sensitive)
- Budget constrained

### Project Ini: ✅ Menggunakan Microservices
- Educational purpose (learn modern architecture)
- Clear separation: CRUD vs Search
- Different database technologies
- Demonstrates real-world scenario
- Scalable untuk future enhancements