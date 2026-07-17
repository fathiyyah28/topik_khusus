# DOCKER & DOCKER COMPOSE

## Apa itu Docker?

### Definisi
Docker adalah platform containerization yang memungkinkan developer untuk mengemas aplikasi beserta semua dependenciesnya (libraries, runtime, environment variables, configuration files) ke dalam container yang ringan, portable, dan self-contained.

### Analogi Sederhana
```
Traditional Deployment (Tanpa Docker):
┌─────────────────────────────────────────┐
│  Developer Machine                      │
│  - Python 3.12                          │
│  - FastAPI 0.104                        │
│  - MongoDB 7.0                          │
│  - Elasticsearch 8.15                   │
│  - Specific OS configuration            │
└─────────────────────────────────────────┘
         │
         │ Deploy to Production
         ▼
┌─────────────────────────────────────────┐
│  Production Server                      │
│  - Python 3.10 (different!)             │
│  - FastAPI 0.100 (different!)           │
│  - Missing library                       │
│  - Different OS configuration            │
│  ❌ "It works on my machine"             │
└─────────────────────────────────────────┘

Docker Deployment:
┌─────────────────────────────────────────┐
│  Developer Machine                      │
│  Dockerfile:                            │
│  - FROM python:3.12-slim                │
│  - RUN pip install fastapi==0.104       │
│  - COPY app /app                        │
└─────────────────────────────────────────┘
         │
         │ docker build
         ▼
┌─────────────────────────────────────────┐
│  Docker Image                           │
│  - Python 3.12 (guaranteed)             │
│  - FastAPI 0.104 (guaranteed)           │
│  - All dependencies included            │
│  - Consistent environment               │
└─────────────────────────────────────────┘
         │
         │ docker run
         ▼
┌─────────────────────────────────────────┐
│  Production Server                      │
│  Container:                             │
│  - Python 3.12 (same!)                  │
│  - FastAPI 0.104 (same!)                │
│  - All dependencies (same!)             │
│  - Identical to development             │
│  ✅ "Works everywhere"                   │
└─────────────────────────────────────────┘
```

---

## Komponen Docker

### 1. Docker Image

#### Definisi
Image adalah blueprint atau template yang berisi semua instructions untuk membuat container. Image adalah read-only template yang defines:
- Base operating system
- Application code
- Dependencies (libraries, packages)
- Environment variables
- Commands to run
- Ports to expose

#### Structure
```
Docker Image
├── Base Layer (OS)
│   └── python:3.12-slim
├── Dependencies Layer
│   └── pip install fastapi uvicorn pymongo
├── Application Layer
│   └── COPY . /app
└── Configuration Layer
    └── CMD ["uvicorn", "app.main:app"]
```

#### Commands
```bash
# List images
docker images

# Pull image dari registry
docker pull python:3.12-slim

# Build image dari Dockerfile
docker build -t myapp:1.0 .

# Tag image
docker tag myapp:1.0 myapp:latest

# Remove image
docker rmi myapp:1.0

# Push to registry
docker push myapp:1.0
```

### 2. Docker Container

#### Definisi
Container adalah instance running dari Docker image. Container adalah isolated process yang berjalan di host machine dengan its own filesystem, networking, dan process space.

#### Characteristics
- **Lightweight**: Shares kernel dengan host (tidak seperti VM)
- **Isolated**: Each container terpisah dari others
- **Portable**: Bisa dijalankan di any machine dengan Docker
- **Ephemeral**: Data hilang jika container dihapus (kecuali menggunakan volumes)

#### Lifecycle
```
Image (Template)
    ↓ docker run
Container (Running instance)
    ↓ docker stop
Container (Stopped)
    ↓ docker start
Container (Running again)
    ↓ docker rm
Deleted
```

#### Commands
```bash
# Run container
docker run -d -p 8001:8001 --name core-service core-service:latest

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop core-service

# Start container
docker start core-service

# Restart container
docker restart core-service

# Remove container
docker rm core-service

# Execute command inside container
docker exec -it core-service bash

# View logs
docker logs core-service

# View logs (follow)
docker logs -f core-service

# Container stats (CPU, memory usage)
docker stats core-service
```

### 3. Docker Volume

#### Definisi
Volume adalah persistent storage untuk data container. Volume memungkinkan data tetap ada meskipun container dihapus atau di-recreate.

#### Use Case
- Database data (MongoDB, Elasticsearch)
- Uploaded files (images, documents)
- Configuration files
- Log files

#### Types of Volumes

##### Named Volume (Managed by Docker)
```bash
# Create volume
docker volume create mongodb_data

# Use volume
docker run -v mongodb_data:/data/db mongo:7

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mongodb_data

# Remove volume
docker volume rm mongodb_data
```

##### Bind Mount (Direct host directory)
```bash
# Mount host directory to container
docker run -v /host/path:/container/path nginx

# Example: Development dengan live reload
docker run -v $(pwd)/app:/app python:3.12
```

#### Docker Compose Volumes
```yaml
services:
  mongodb:
    image: mongo:7
    volumes:
      - mongodb_data:/data/db  # Named volume
      - ./backup:/backup        # Bind mount
  
  elasticsearch:
    image: elasticsearch:8.15.0
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

volumes:
  mongodb_data:
    driver: local
  elasticsearch_data:
    driver: local
```

### 4. Docker Network

#### Definisi
Network adalah virtual network yang memungkinkan komunikasi antar containers. Containers dalam network yang sama bisa saling mengakses menggunakan service name.

#### Network Types

##### Bridge Network (Default)
```bash
# Create network
docker network create my-network

# Run container dengan network
docker run --network=my-network --name=container1 nginx
docker run --network=my-network --name=container2 nginx

# Containers bisa communicate via name
# container1 → container2: http://container2:80
```

##### Host Network
```bash
# Container shares host's network
docker run --network=host nginx
# Container accessible via localhost:80
```

##### Overlay Network (Swarm)
```bash
# For multi-host networking (Docker Swarm)
docker network create --driver overlay my-overlay
```

#### Docker Compose Networks
```yaml
services:
  core-service:
    image: core-service:latest
    networks:
      - uas_app-network
  
  search-service:
    image: search-service:latest
    networks:
      - uas_app-network

networks:
  uas_app-network:
    driver: bridge
```

**Benefit**: Containers bisa communicate via service name:
```python
# Core Service mengakses Search Service
url = "http://search-service:8002/api/sync/single"
# Docker DNS resolves "search-service" to IP address
```

### 5. Dockerfile

#### Definisi
Dockerfile adalah text file yang contains instructions untuk build Docker image. Setiap instruction creates a layer dalam image.

#### Instructions

##### FROM
```dockerfile
# Base image
FROM python:3.12-slim
```

##### WORKDIR
```dockerfile
# Set working directory
WORKDIR /app
```

##### COPY
```dockerfile
# Copy files from host to container
COPY requirements.txt .
COPY . .
```

##### RUN
```dockerfile
# Execute command during build
RUN pip install --no-cache-dir -r requirements.txt
```

##### ENV
```dockerfile
# Set environment variables
ENV MONGO_URI=mongodb://mongodb:27017
ENV DATABASE_NAME=uas_db
```

##### EXPOSE
```dockerfile
# Document exposed ports
EXPOSE 8001
```

##### CMD
```dockerfile
# Default command when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

##### ENTRYPOINT
```dockerfile
# Entry point script
ENTRYPOINT ["docker-entrypoint.sh"]
```

#### Example Dockerfiles

**Core Service** (`core-service/Dockerfile`):
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Frontend** (`frontend/Dockerfile`):
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build application
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

### 6. Docker Compose

#### Definisi
Docker Compose adalah tool untuk defining dan running multi-container Docker applications. Dengan single YAML file, seluruh stack aplikasi bisa dijalankan dengan single command.

#### File Structure
```
project/
├── docker-compose.yml
├── core-service/
│   ├── Dockerfile
│   └── app/
├── search-service/
│   ├── Dockerfile
│   └── app/
└── frontend/
    ├── Dockerfile
    └── src/
```

#### Example docker-compose.yml
```yaml
version: '3.8'

services:
  # Core Service
  core-service:
    build: ./core-service
    ports:
      - "8001:8001"
    environment:
      - MONGO_URI=mongodb://mongodb:27017
      - SEARCH_SERVICE_URL=http://search-service:8002
    depends_on:
      mongodb:
        condition: service_healthy
      search-service:
        condition: service_healthy
    networks:
      - uas_app-network
    restart: unless-stopped

  # Search Service
  search-service:
    build: ./search-service
    ports:
      - "8002:8002"
    environment:
      - ELASTIC_URI=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - uas_app-network
    restart: unless-stopped

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - core-service
      - search-service
    networks:
      - uas_app-network
    restart: unless-stopped

  # MongoDB
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=uas_db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - uas_app-network
    restart: unless-stopped

  # Elasticsearch
  elasticsearch:
    image: elasticsearch:8.15.0
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200/_cluster/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - uas_app-network
    restart: unless-stopped

# Networks
networks:
  uas_app-network:
    driver: bridge

# Volumes
volumes:
  mongodb_data:
    driver: local
  elasticsearch_data:
    driver: local
```

---

## Docker Compose Commands

### Basic Commands
```bash
# Start all services (detached mode)
docker-compose up -d

# Start specific service
docker-compose up -d core-service

# Stop all services
docker-compose down

# Stop specific service
docker-compose stop core-service

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart core-service

# View logs
docker-compose logs

# View logs (follow)
docker-compose logs -f

# View logs for specific service
docker-compose logs -f core-service

# List running services
docker-compose ps

# Execute command in service
docker-compose exec core-service bash

# Run command in service (one-off)
docker-compose run --rm core-service python --version
```

### Build Commands
```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build core-service

# Build without cache
docker-compose build --no-cache

# Build and start
docker-compose up -d --build
```

### Advanced Commands
```bash
# Scale service (multiple instances)
docker-compose up -d --scale core-service=3

# Pull latest images
docker-compose pull

# Validate compose file
docker-compose config

# View service dependencies
docker-compose depends_on
```

---

## Health Checks

### Definisi
Health checks adalah mekanisme untuk memastikan container sudah siap dan berjalan dengan baik sebelum menerima traffic.

### Implementation

#### Docker Compose Health Check
```yaml
services:
  mongodb:
    image: mongo:7
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s      # Check every 10 seconds
      timeout: 5s        # Timeout after 5 seconds
      retries: 5         # Retry 5 times before marking unhealthy
      start_period: 30s  # Grace period for startup
```

#### Application Health Check
```python
# app/health.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "core-service",
        "version": "1.0.0"
    }
```

```yaml
services:
  core-service:
    build: ./core-service
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 10s
      timeout: 5s
      retries: 3
```

---

## Mengapa Docker Digunakan?

### 1. Consistency
```
Problem: "It works on my machine"
Solution: Docker ensures same environment everywhere

Development:
  - Docker Desktop (Windows/Mac)
  - Docker Engine (Linux)

Staging:
  - Same Docker images
  - Same configuration

Production:
  - Same Docker images
  - Same configuration

Result: No more "works on my machine" issues
```

### 2. Isolation
```
Each service runs in its own container:
- Core Service: Container 1
- Search Service: Container 2
- MongoDB: Container 3
- Elasticsearch: Container 4

Benefits:
- No conflicts between services
- Independent resource allocation
- Separate logging
- Individual scaling
```

### 3. Portability
```
"Build once, run anywhere"

Developer's Laptop:
  docker run myapp:latest

Testing Server:
  docker run myapp:latest

Production Server:
  docker run myapp:latest

Cloud (AWS/GCP/Azure):
  docker run myapp:latest

Same image, same behavior everywhere
```

### 4. Easy Setup
```bash
# Traditional setup (hours):
1. Install Python 3.12
2. Install MongoDB 7.0
3. Install Elasticsearch 8.15
4. Configure each service
5. Setup networking
6. Configure environment variables
7. Test connections
8. Debug issues

# Docker setup (minutes):
docker-compose up -d

Done! All services running.
```

### 5. Version Control
```bash
# Dockerfile bisa di-commit ke Git
git add Dockerfile docker-compose.yml
git commit -m "Add containerization"

# Team members get exact same environment
git pull
docker-compose up -d

# Rollback to previous version
git checkout v1.0
docker-compose up -d
```

### 6. Resource Efficiency
```
Virtual Machines:
- Each VM: Full OS (GBs of disk, GBs of RAM)
- Slow startup (minutes)
- Heavy resource usage

Docker Containers:
- Share host kernel (MBs of disk, MBs of RAM)
- Fast startup (seconds)
- Lightweight resource usage

Comparison:
- VM: 1-2 GB per instance
- Container: 50-100 MB per instance
- 10-20x more efficient
```

---

## Docker vs Virtual Machines

| Aspek | Docker | Virtual Machine |
|-------|--------|-----------------|
| **OS** | Shares host kernel | Full OS per VM |
| **Size** | MBs | GBs |
| **Startup** | Seconds | Minutes |
| **Performance** | Near native | Slower (hypervisor overhead) |
| **Isolation** | Process-level | Full OS isolation |
| **Resource Usage** | Low | High |
| **Density** | High (100+ per host) | Low (10-20 per host) |
| **Portability** | Very portable | Less portable |

---

## Docker Best Practices

### 1. Image Optimization
```dockerfile
# ❌ BAD: Large image
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
COPY . .
CMD ["python3", "app.py"]

# ✅ GOOD: Small image
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### 2. Layer Caching
```dockerfile
# ✅ GOOD: Dependencies first (cached)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ BAD: Code first (cache invalidated on every change)
COPY . .
RUN pip install -r requirements.txt
```

### 3. Multi-Stage Builds
```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

### 4. Security
```dockerfile
# ✅ GOOD: Non-root user
FROM python:3.12-slim
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# ❌ BAD: Running as root
FROM python:3.12-slim
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### 5. Environment Variables
```dockerfile
# ✅ GOOD: Use ENV for configuration
ENV MONGO_URI=mongodb://mongodb:27017
ENV DATABASE_NAME=uas_db

# Override at runtime
# docker run -e MONGO_URI=mongodb://localhost:27017 myapp
```

---

## Docker dalam Project Ini

### Architecture
```
┌─────────────────────────────────────────────┐
│         Docker Compose Stack                │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ core-service │  │search-service│        │
│  │  (FastAPI)   │  │  (FastAPI)   │        │
│  │  Port: 8001  │  │  Port: 8002  │        │
│  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                │
│  ┌──────▼───────┐  ┌──────▼───────┐        │
│  │   MongoDB    │  │ Elasticsearch│        │
│  │  Port: 27017 │  │  Port: 9200  │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
│  ┌──────────────┐                           │
│  │   Frontend   │                           │
│  │  Port: 3000  │                           │
│  └──────────────┘                           │
│                                             │
│  Network: uas_app-network (bridge)          │
│                                             │
│  Volumes:                                   │
│  - mongodb_data                            │
│  - elasticsearch_data                       │
└─────────────────────────────────────────────┘
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  core-service:
    build: ./core-service
    ports:
      - "8001:8001"
    environment:
      - MONGO_URI=mongodb://mongodb:27017
      - SEARCH_SERVICE_URL=http://search-service:8002
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - uas_app-network

  search-service:
    build: ./search-service
    ports:
      - "8002:8002"
    environment:
      - ELASTIC_URI=http://elasticsearch:9200
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - uas_app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - core-service
      - search-service
    networks:
      - uas_app-network

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
    networks:
      - uas_app-network

  elasticsearch:
    image: elasticsearch:8.15.0
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200"]
    networks:
      - uas_app-network

networks:
  uas_app-network:
    driver: bridge

volumes:
  mongodb_data:
  elasticsearch_data:
```

### Commands Used in Project
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f core-service

# Restart service after code changes
docker-compose restart core-service

# Rebuild after Dockerfile changes
docker-compose build core-service
docker-compose up -d core-service

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: Port 8001 already allocated
# Solution: Change port in docker-compose.yml
ports:
  - "8001:8001"  # Change to "8003:8001"
```

#### 2. Container Keeps Restarting
```bash
# Check logs
docker-compose logs core-service

# Common causes:
# - Application error
# - Port conflict
# - Missing environment variables
# - Database not ready
```

#### 3. Cannot Connect to Database
```bash
# Check if database is healthy
docker-compose ps

# Check network
docker network inspect uas_app-network

# Test connection from container
docker-compose exec core-service ping mongodb
```

#### 4. Out of Disk Space
```bash
# Clean up unused images, containers, volumes
docker system prune -a

# Remove specific volume
docker volume rm uas_mongodb_data
```

---

## Docker Commands Reference

### Image Management
```bash
docker images                    # List images
docker pull <image>              # Pull image
docker build -t <name> .         # Build image
docker tag <src> <dest>          # Tag image
docker push <image>              # Push to registry
docker rmi <image>               # Remove image
```

### Container Management
```bash
docker ps                        # List running containers
docker ps -a                     # List all containers
docker run <image>               # Run container
docker stop <container>          # Stop container
docker start <container>         # Start container
docker restart <container>       # Restart container
docker rm <container>            # Remove container
docker exec -it <container> bash # Execute in container
docker logs <container>          # View logs
docker stats <container>         # View stats
```

### Volume Management
```bash
docker volume ls                 # List volumes
docker volume create <name>      # Create volume
docker volume inspect <name>     # Inspect volume
docker volume rm <name>          # Remove volume
```

### Network Management
```bash
docker network ls                # List networks
docker network create <name>     # Create network
docker network inspect <name>    # Inspect network
docker network rm <name>         # Remove network
```

### System Management
```bash
docker info                      # System info
docker version                   # Version info
docker system prune              # Clean up unused resources
docker system df                 # Disk usage
```

---

## Docker dalam Development vs Production

### Development
```yaml
services:
  core-service:
    build:
      context: ./core-service
      dockerfile: Dockerfile.dev
    volumes:
      - ./core-service:/app  # Live reload
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    ports:
      - "8001:8001"
```

### Production
```yaml
services:
  core-service:
    image: core-service:1.0.0  # Use specific version
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## Kesimpulan

Docker adalah tool essential untuk modern software development yang provides:
- **Consistency**: Same environment everywhere
- **Isolation**: Services terpisah dan independent
- **Portability**: Run anywhere
- **Efficiency**: Lightweight dan fast
- **Scalability**: Easy to scale

Untuk project ini, Docker memastikan bahwa semua services (Core, Search, MongoDB, Elasticsearch, Frontend) bisa dijalankan dengan single command `docker-compose up -d` tanpa perlu manual setup yang complex.