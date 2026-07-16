# BAB 7: ARSITEKTUR SISTEM

## 7.1 Arsitektur Umum

Sistem Mongo Search Portal menggunakan arsitektur **microservice** dengan tiga komponen utama yang berjalan dalam container Docker.

```mermaid
graph TB
    subgraph "Client"
        A[Browser]
    end

    subgraph "Docker Compose Network"
        subgraph "Frontend Layer"
            B[Vue.js 3 App<br/>Port 3000]
        end

        subgraph "Backend Layer"
            C[Core Service<br/>FastAPI | Port 8001]
            D[Search Service<br/>FastAPI | Port 8002]
        end

        subgraph "Database Layer"
            E[(MongoDB 7<br/>Port 27017)]
            F[(Elasticsearch 8.15<br/>Port 9200)]
        end

        subgraph "Volume Storage"
            G[mongodb_data<br/>Volume]
            H[elasticsearch_data<br/>Volume]
        end
    end

    A -->|HTTP| B
    B -->|REST API| C
    B -->|REST API| D
    C -->|CRUD| E
    C -->|HTTP Sync| D
    D -->|Full-Text Search| F
    E --> G
    F --> H

    style A fill:#e1f5fe
    style B fill:#42b883,color:#fff
    style C fill:#009688,color:#fff
    style D fill:#ff6f00,color:#fff
    style E fill:#4db33d,color:#fff
    style F fill:#00bfb3,color:#fff
```

## 7.2 Arsitektur Microservice

### 7.2.1 Pembagian Service

| Service | Bahasa | Framework | Database | Port |
|---------|--------|-----------|----------|------|
| Frontend | JavaScript | Vue.js 3 + Vite | - | 3000 |
| Core Service | Python | FastAPI | MongoDB | 8001 |
| Search Service | Python | FastAPI | Elasticsearch | 8002 |

### 7.2.2 Karakteristik Microservice

| Karakteristik | Implementasi |
|---------------|--------------|
| **Deployment Independence** | Setiap service memiliki Dockerfile sendiri |
| **Database Independence** | Core Service menggunakan MongoDB, Search Service menggunakan Elasticsearch |
| **Communication** | Frontend → Backend via HTTP REST, Core → Search via HTTP |
| **Technology Diversity** | Vue.js (frontend), Python/FastAPI (backend) |
| **Scalability** | Setiap service dapat di-scale secara independen |

## 7.3 Arsitektur Core Service

```mermaid
graph TD
    subgraph "Core Service (FastAPI)"
        A[main.py<br/>FastAPI App]
        B[routes.py<br/>API Endpoints]
        C[mongo_service.py<br/>MongoDB Operations]
        D[schemas.py<br/>Pydantic Models]
        E[config.py<br/>Environment Config]
        
        A --> B
        B --> C
        B --> D
        A --> E
    end

    subgraph "External"
        F[Frontend]
        G[(MongoDB)]
        H[Search Service]
    end

    F -->|HTTP| B
    B -->|CRUD| C
    C -->|pymongo| G
    B -->|httpx sync| H
```

### 7.2.2 Alur Request

```mermaid
sequenceDiagram
    participant Client as Browser
    participant FastAPI as FastAPI App
    participant Routes as routes.py
    participant Service as mongo_service.py
    participant DB as MongoDB

    Client->>FastAPI: HTTP Request
    FastAPI->>Routes: Route Handler
    Routes->>Service: Function Call
    Service->>DB: pymongo Query
    DB-->>Service: Result
    Service-->>Routes: Data
    Routes-->>FastAPI: Response
    FastAPI-->>Client: JSON Response
```

## 7.4 Arsitektur Search Service

```mermaid
graph TD
    subgraph "Search Service (FastAPI)"
        A[main.py<br/>FastAPI App]
        B[routes.py<br/>API Endpoints]
        C[elastic_service.py<br/>ES Operations]
        D[schemas.py<br/>Pydantic Models]
        E[config.py<br/>Environment Config]
        
        A --> B
        B --> C
        B --> D
        A --> E
    end

    subgraph "External"
        F[Frontend]
        G[Core Service]
        H[(Elasticsearch)]
    end

    F -->|HTTP Search| B
    G -->|HTTP Sync| B
    B -->|elasticsearch-py| H
```

## 7.5 Arsitektur Frontend

```mermaid
graph TD
    subgraph "Frontend (Vue.js 3)"
        A[main.js<br/>Entry Point]
        B[App.vue<br/>Layout]
        C[router/index.js<br/>Routing]
        D[services/api.js<br/>Axios Client]
        
        subgraph "Components"
            E[Navbar.vue]
            F[Footer.vue]
            G[Loading.vue]
            H[ProductTable.vue]
            I[ProductModal.vue]
            J[SearchBar.vue]
            K[SearchCard.vue]
        end
        
        subgraph "Pages"
            L[Home.vue]
            M[Products.vue]
            N[Search.vue]
        end
    end

    A --> B
    B --> C
    B --> D
    B --> E
    B --> F
    C --> L
    C --> M
    C --> N
    M --> H
    M --> I
    M --> G
    N --> J
    N --> K
    N --> G
```

## 7.6 Arsitektur Deployment (Docker)

```mermaid
graph TD
    subgraph "Docker Compose"
        subgraph "Network: app-network"
            A[frontend<br/>nginx: alpine]
            B[core-service<br/>python:3.12-slim]
            C[search-service<br/>python:3.12-slim]
            D[mongodb<br/>mongo:7]
            E[elasticsearch<br/>elasticsearch:8.15]
        end
        
        subgraph "Volumes"
            F[mongodb_data]
            G[elasticsearch_data]
        end
    end

    A -->|depends_on| B
    A -->|depends_on| C
    B -->|depends_on| D
    C -->|depends_on| E
    D --> F
    E --> G

    style A fill:#42b883,color:#fff
    style B fill:#009688,color:#fff
    style C fill:#ff6f00,color:#fff
    style D fill:#4db33d,color:#fff
    style E fill:#00bfb3,color:#fff
```

### 7.6.1 Port Mapping

| Container | Internal Port | Host Port | Protocol |
|-----------|---------------|-----------|----------|
| frontend | 3000 | 3000 | TCP |
| core-service | 8001 | 8001 | TCP |
| search-service | 8002 | 8002 | TCP |
| mongodb | 27017 | 27017 | TCP |
| elasticsearch | 9200 | 9200 | TCP |

### 7.6.2 Volume Mapping

| Volume | Container Path | Deskripsi |
|--------|---------------|-----------|
| mongodb_data | /data/db | Data persistence MongoDB |
| elasticsearch_data | /usr/share/elasticsearch/data | Data persistence Elasticsearch |

### 7.6.3 Environment Variable Flow

```mermaid
flowchart LR
    A[.env file] --> B[Docker Compose]
    B -->|MONGO_HOST=mongodb| C[Core Service]
    B -->|ELASTIC_HOST=elasticsearch| D[Search Service]
    B -->|VITE_CORE_SERVICE_URL| E[Frontend Build]
    C -->|SEARCH_SERVICE_URL| D
    C -->|MONGO_HOST=mongodb| F[(MongoDB)]
    D -->|ELASTIC_HOST=elasticsearch| G[(Elasticsearch)]
```

## 7.7 Komunikasi Antar Service

### 7.7.1 Frontend → Core Service

- **Protokol**: HTTP REST
- **Format**: JSON
- **Endpoint**: `http://core-service:8001/api/*`
- **Fungsi**: CRUD produk

### 7.7.2 Frontend → Search Service

- **Protokol**: HTTP REST
- **Format**: JSON
- **Endpoint**: `http://search-service:8002/api/*`
- **Fungsi**: Pencarian full-text

### 7.7.3 Core Service → Search Service (Sync)

- **Protokol**: HTTP REST (httpx async)
- **Format**: JSON
- **Endpoint**: `/api/sync`, `/api/sync/{id}`
- **Trigger**: Operasi create, update, delete data
- **Fault Tolerance**: Jika Search Service offline, CRUD tetap berjalan (sync gagal dilewati)

## 7.8 Sequence Diagram: CRUD Product

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Core as Core Service
    participant Search as Search Service
    participant Mongo as MongoDB
    participant ES as Elasticsearch

    Note over User,ES: CREATE PRODUCT
    User->>Frontend: Klik Tambah Produk
    Frontend->>Frontend: Buka Modal Form
    User->>Frontend: Isi Form & Submit
    Frontend->>Core: POST /api/products {data}
    Core->>Mongo: insert_one(data)
    Mongo-->>Core: success
    Core->>Search: POST /api/sync {data}
    Search->>ES: index document
    ES-->>Search: success
    Search-->>Core: 201 Created
    Core-->>Frontend: 201 Created
    Frontend-->>User: Toast Sukses

    Note over User,ES: UPDATE PRODUCT
    User->>Frontend: Klik Edit
    Frontend->>Frontend: Buka Modal Edit
    User->>Frontend: Ubah Data & Submit
    Frontend->>Core: PUT /api/products/{id} {data}
    Core->>Mongo: update_one({_id: id}, {$set: data})
    Mongo-->>Core: success
    Core->>Search: PUT /api/sync/{id} {data}
    Search->>ES: update document
    ES-->>Search: success
    Search-->>Core: 200 OK
    Core-->>Frontend: 200 OK
    Frontend-->>User: Toast Sukses

    Note over User,ES: DELETE PRODUCT
    User->>Frontend: Klik Hapus
    Frontend->>Frontend: Buka Konfirmasi
    User->>Frontend: Konfirmasi Hapus
    Frontend->>Core: DELETE /api/products/{id}
    Core->>Mongo: delete_one({_id: id})
    Mongo-->>Core: success
    Core->>Search: DELETE /api/sync/{id}
    Search->>ES: delete document
    ES-->>Search: success
    Search-->>Core: 200 OK
    Core-->>Frontend: 200 OK
    Frontend-->>User: Toast Sukses
```

## 7.9 Sequence Diagram: Search Product

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Search as Search Service
    participant ES as Elasticsearch

    Note over User,ES: SEARCH FLOW
    User->>Frontend: Ketik kata kunci
    User->>Frontend: Klik Cari / Enter
    Frontend->>Frontend: Tampilkan Loading
    Frontend->>Search: GET /api/search?q=keyword
    Search->>ES: multi_match query
    Note over Search,ES: fields: [nama, kategori, spesifikasi]
    ES-->>Search: hits results
    Search-->>Frontend: {status, data, total, keyword}
    Frontend->>Frontend: Render Cards
    Frontend-->>User: Tampilkan Hasil
```

## 7.10 Stack Teknologi

```mermaid
graph LR
    subgraph "Frontend"
        A1[Vue.js 3]
        A2[Vite]
        A3[Bootstrap 5]
        A4[Axios]
        A5[Vue Router]
    end

    subgraph "Backend Core"
        B1[Python 3.12]
        B2[FastAPI]
        B3[Uvicorn]
        B4[PyMongo]
        B5[Pydantic]
        B6[httpx]
    end

    subgraph "Backend Search"
        C1[Python 3.12]
        C2[FastAPI]
        C3[Uvicorn]
        C4[elasticsearch-py]
        C5[Pydantic]
    end

    subgraph "Database"
        D1[MongoDB 7]
        D2[Elasticsearch 8.15]
    end

    subgraph "DevOps"
        E1[Docker]
        E2[Docker Compose]
    end

    A1 --> A2
    A1 --> A3
    A1 --> A4
    A1 --> A5
    
    B2 --> B3
    B2 --> B4
    B2 --> B5
    B2 --> B6
    
    C2 --> C3
    C2 --> C4
    C2 --> C5
    
    B4 --> D1
    C4 --> D2
    
    E1 --> E2
    E2 --> B2
    E2 --> C2
    E2 --> A1
    E2 --> D1
    E2 --> D2