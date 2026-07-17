# ALUR SEARCH

## Overview
Bagian ini menjelaskan alur pencarian (search) secara detail, dari input user hingga hasil yang ditampilkan. Search adalah fitur utama yang membedakan sistem ini dari aplikasi CRUD biasa.

---

## Search System Overview

```
User Input: "laptop gaming"
    ↓
Frontend (Vue.js)
    ↓
Search Service (FastAPI)
    ↓
Elasticsearch (Search Engine)
    ↓
Inverted Index Lookup
    ↓
Relevance Scoring
    ↓
Sorted Results
    ↓
Return to User
```

---

## 1. Search Flow Diagram

### High-Level Flow
```
┌──────────┐
│  User    │
│  Types:  │
│ "laptop" │
└────┬─────┘
     │
     │ 1. Input
     ▼
┌─────────────────────┐
│   Frontend          │
│   (Vue.js)          │
│                     │
│  - Debounce 300ms   │
│  - Send request     │
└────┬────────────────┘
     │
     │ 2. GET /api/search?q=laptop
     ▼
┌─────────────────────┐
│   Search Service    │
│   (FastAPI)         │
│   Port: 8002        │
└────┬────────────────┘
     │
     │ 3. Analyze query
     ▼
┌─────────────────────┐
│   Elasticsearch     │
│                     │
│  - Tokenize         │
│  - Lookup index     │
│  - Calculate scores │
└────┬────────────────┘
     │
     │ 4. Return results
     ▼
┌─────────────────────┐
│   Search Service    │
│                     │
│  - Format response  │
└────┬────────────────┘
     │
     │ 5. JSON response
     ▼
┌─────────────────────┐
│   Frontend          │
│                     │
│  - Display results  │
│  - Highlight match  │
└────┬────────────────┘
     │
     │ 6. User sees results
     ▼
┌──────────┐
│  User    │
│  Views   │
│  Results │
└──────────┘
```

---

## 2. Detailed Search Flow

### 2.1 User Input & Debouncing

#### Frontend Implementation
```javascript
// SearchBar.vue
import { ref, watch } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// Debounce search (wait 300ms after typing stops)
watch(searchQuery, (newQuery) => {
  if (newQuery.length < 2) {
    searchResults.value = []
    return
  }
  
  // Debounce
  setTimeout(async () => {
    await performSearch(newQuery)
  }, 300)
})

async function performSearch(query) {
  isSearching.value = true
  
  try {
    const response = await axios.get('http://localhost:8002/api/search', {
      params: { q: query }
    })
    
    searchResults.value = response.data.data
    totalResults.value = response.data.total
  } catch (error) {
    console.error('Search failed:', error)
    searchResults.value = []
  } finally {
    isSearching.value = false
  }
}
```

#### Why Debounce?
```
User typing: "laptop gaming"
    ↓
Without debounce:
  - "l" → search
  - "la" → search
  - "lap" → search
  - "lapt" → search
  - "lapto" → search
  - "laptop" → search
  - "laptop " → search
  - "laptop g" → search
  - ... (12 requests)
  
With debounce (300ms):
  - User types "laptop gaming"
  - Waits 300ms
  - "laptop gaming" → search (1 request)
  
Benefit:
- Reduce server load
- Better UX (no flickering results)
- More efficient
```

---

### 2.2 Search Service - Receive Query

#### API Endpoint
```python
# search-service/app/routes.py
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=1, description="Kata kunci pencarian")
):
    """
    Search endpoint
    - q: Search query (minimum 1 character)
    """
    try:
        # Check Elasticsearch connection
        if not es.cek_koneksi():
            raise HTTPException(
                status_code=503,
                detail="Elasticsearch tidak tersedia"
            )
        
        # Execute search
        hasil = es.cari_match(q)
        
        return {
            "status": "success",
            "message": f"Ditemukan {len(hasil)} hasil untuk '{q}'",
            "data": hasil,
            "total": len(hasil),
            "keyword": q
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error search_products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 2.3 Elasticsearch - Query Execution

#### Search Implementation
```python
# search-service/app/elastic_service.py
def cari_match(keyword: str) -> List[Dict[str, Any]]:
    """
    Search products using multi-match query
    
    Args:
        keyword: Search keyword
    
    Returns:
        List of matching products
    """
    client = dapatkan_koneksi()
    
    try:
        # Build query
        query = {
            "query": {
                "multi_match": {
                    "query": keyword,  # "laptop gaming"
                    "fields": ["nama", "kategori", "spesifikasi"],
                    "type": "best_fields"
                }
            }
        }
        
        # Execute search
        response = client.search(
            index=ELASTIC_INDEX_NAME,
            body=query
        )
        
        # Extract results
        hits = response["hits"]["hits"]
        data = [hit["_source"] for hit in hits]
        
        logger.info(f"Pencarian ES '{keyword}': {len(data)} hasil.")
        return data
    except NotFoundError:
        logger.warning(f"Index '{ELASTIC_INDEX_NAME}' tidak ditemukan.")
        return []
    except Exception as e:
        logger.error(f"Gagal mencari data: {e}")
        return []
```

---

## 3. Elasticsearch Search Process

### 3.1 Query Analysis

#### Input
```
User Query: "laptop gaming"
```

#### Analysis Process
```
Step 1: Lowercase
  "laptop gaming" → "laptop gaming"

Step 2: Tokenization
  "laptop gaming" → ["laptop", "gaming"]

Step 3: Stopwords (if any)
  ["laptop", "gaming"] → ["laptop", "gaming"] (no stopwords)

Final Tokens: ["laptop", "gaming"]
```

### 3.2 Inverted Index Lookup

#### Inverted Index Structure
```
Token      → Document IDs
"laptop"   → [1, 5, 12, 23, 45]
"gaming"   → [5, 12, 23]
"asus"     → [1, 12]
"terbaik"  → [5, 12, 23, 45]
```

#### Lookup Process
```
Query Tokens: ["laptop", "gaming"]

Lookup "laptop":
  → [1, 5, 12, 23, 45]

Lookup "gaming":
  → [5, 12, 23]

Merge (AND operation):
  Intersection: [5, 12, 23]

Matching Documents: 5, 12, 23
```

### 3.3 Relevance Scoring

#### BM25 Scoring Algorithm
```
Score = IDF × TF

IDF (Inverse Document Frequency):
  IDF(term) = log((N - n(term) + 0.5) / (n(term) + 0.5) + 1)
  
  Where:
  - N = total documents
  - n(term) = documents containing term

TF (Term Frequency):
  TF(term, doc) = (freq(term) * (k1 + 1)) / (freq(term) + k1 * (1 - b + b * doc_len / avg_doc_len))
  
  Where:
  - freq(term) = frequency of term in document
  - k1 = 1.2 (default)
  - b = 0.75 (default)
  - doc_len = document length
  - avg_doc_len = average document length
```

#### Example Calculation
```
Document 5: "Laptop Gaming Asus ROG"
  - Contains: "laptop" (1x), "gaming" (1x)
  - Length: 4 words
  
Document 12: "Laptop Gaming Terbaik"
  - Contains: "laptop" (1x), "gaming" (1x)
  - Length: 3 words

Document 23: "Gaming Laptop"
  - Contains: "laptop" (1x), "gaming" (1x)
  - Length: 2 words

Total docs: 100
Docs with "laptop": 50
Docs with "gaming": 30

IDF("laptop") = log((100 - 50 + 0.5) / (50 + 0.5) + 1) = 0.69
IDF("gaming") = log((100 - 30 + 0.5) / (30 + 0.5) + 1) = 1.20

Score Calculation:
Doc 5:  IDF(laptop) * TF(laptop) + IDF(gaming) * TF(gaming)
      = 0.69 * 1.0 + 1.20 * 1.0
      = 1.89

Doc 12: Similar calculation
       = 1.85

Doc 23: Similar calculation
       = 1.82

Ranking: Doc 5 (1.89) > Doc 12 (1.85) > Doc 23 (1.82)
```

### 3.4 Result Sorting & Pagination

#### Sorting
```python
# Elasticsearch automatically sorts by score (descending)
# Highest score = most relevant

# Results
[
  {
    "_id": 5,
    "_score": 1.89,
    "_source": {
      "nama": "Laptop Gaming Asus ROG",
      "kategori": "Laptop",
      "harga": 18999000,
      ...
    }
  },
  {
    "_id": 12,
    "_score": 1.85,
    "_source": {
      "nama": "Laptop Gaming Terbaik",
      "kategori": "Laptop",
      "harga": 15999000,
      ...
    }
  },
  ...
]
```

#### Pagination (Future Enhancement)
```python
# Add pagination to query
query = {
    "query": {
        "multi_match": {
            "query": keyword,
            "fields": ["nama", "kategori", "spesifikasi"]
        }
    },
    "from": 0,  # Offset (page 1 = 0)
    "size": 10  # Limit (10 results per page)
}

# Page 1: from=0, size=10
# Page 2: from=10, size=10
# Page 3: from=20, size=10
```

---

## 4. Search Features

### 4.1 Full-Text Search

#### Multi-Field Search
```python
# Search across multiple fields
query = {
    "query": {
        "multi_match": {
            "query": "laptop gaming",
            "fields": ["nama", "kategori", "spesifikasi"],
            "type": "best_fields"  # Use best matching field
        }
    }
}

# Example:
# Document 1: nama="Laptop Gaming", kategori="Laptop"
# Document 2: nama="Phone", spesifikasi="Gaming Phone"
# 
# Query "laptop gaming" matches:
# - Document 1: matches in "nama" field (best)
# - Document 2: matches in "spesifikasi" field
```

#### Search Types
```python
# 1. best_fields (default)
# - Find best matching field
# - Use for: general search

# 2. most_fields
# - Match across multiple fields
# - Use for: multi-field search

# 3. cross_fields
# - Treat fields as unified
# - Use for: name + address search

# 4. phrase
# - Exact phrase matching
# - Use for: exact phrase search

# 5. phrase_prefix
# - Last word is prefix
# - Use for: autocomplete
```

### 4.2 Fuzzy Matching

#### Example
```python
# User types: "lapto" (typo)
# Elasticsearch matches: "laptop" (edit distance 1)

query = {
    "query": {
        "fuzzy": {
            "nama": {
                "value": "lapto",
                "fuzziness": "AUTO"  # Auto determine edit distance
            }
        }
    }
}

# Fuzziness levels:
# - 0: Exact match
# - 1: One character difference
# - 2: Two character difference
# - AUTO: Based on term length
```

### 4.3 Phrase Search

#### Example
```python
# User searches: "laptop gaming"
# Match exact phrase (words in sequence)

query = {
    "query": {
        "match_phrase": {
            "nama": "laptop gaming"
        }
    }
}

# Matches:
# - "Laptop Gaming Asus" ✓
# - "Gaming Laptop Asus" ✗ (wrong order)
```

### 4.4 Boolean Search

#### Example
```python
# Complex search with AND, OR, NOT

query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"nama": "laptop"}}  # MUST match
            ],
            "should": [
                {"match": {"kategori": "gaming"}}  # SHOULD match (boost)
            ],
            "must_not": [
                {"match": {"stok": 0}}  # MUST NOT match (out of stock)
            ],
            "filter": [
                {"range": {"harga": {"lte": 10000000}}}  # Filter by price
            ]
        }
    }
}

# Result:
# - Must have "laptop" in name
# - Boost if "gaming" in category
# - Exclude if out of stock
# - Price <= 10,000,000
```

---

## 5. Search vs MongoDB Regex

### 5.1 MongoDB Regex Search (Old Way)

#### Implementation
```python
# MongoDB regex search
def cari_regex(keyword: str):
    import re
    pattern = re.compile(keyword, re.IGNORECASE)
    
    query = {
        "$or": [
            {"nama": {"$regex": pattern}},
            {"kategori": {"$regex": pattern}},
            {"spesifikasi": {"$regex": pattern}}
        ]
    }
    
    data = list(collection.find(query))
    return data
```

#### Problems
```
❌ Full Collection Scan
   - Must scan ALL documents
   - O(n) complexity
   - Slow for large datasets

❌ No Relevance Scoring
   - All matches equal
   - No ranking

❌ No Fuzzy Matching
   - Exact pattern only
   - "lapto" won't match "laptop"

❌ No Stemming
   - "laptop" ≠ "laptops"
   - Must match exactly

❌ CPU Intensive
   - High CPU usage
   - Blocks other operations

Performance:
- 1,000 docs: ~50ms
- 10,000 docs: ~500ms
- 100,000 docs: ~5,000ms (5 seconds!)
```

### 5.2 Elasticsearch Search (New Way)

#### Implementation
```python
# Elasticsearch search
def cari_match(keyword: str):
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["nama", "kategori", "spesifikasi"],
                "type": "best_fields"
            }
        }
    }
    
    response = client.search(index="produk", body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]
```

#### Advantages
```
✅ Inverted Index
   - Direct lookup
   - O(1) complexity
   - Fast regardless of dataset size

✅ Relevance Scoring
   - BM25 algorithm
   - Ranked results
   - Most relevant first

✅ Fuzzy Matching
   - Tolerates typos
   - "lapto" matches "laptop"

✅ Stemming
   - "laptop" matches "laptops"
   - Language-aware

✅ Efficient
   - Low CPU usage
   - Non-blocking

Performance:
- 1,000 docs: ~10ms
- 10,000 docs: ~15ms
- 1,000,000 docs: ~50ms
```

### 5.3 Comparison Table

| Aspek | MongoDB Regex | Elasticsearch |
|-------|---------------|---------------|
| **Speed** | O(n) - Linear | O(1) - Constant |
| **10,000 docs** | ~500ms | ~15ms |
| **100,000 docs** | ~5,000ms | ~20ms |
| **1,000,000 docs** | ~50,000ms | ~50ms |
| **Relevance Scoring** | ❌ No | ✅ Yes (BM25) |
| **Fuzzy Matching** | ❌ No | ✅ Yes |
| **Stemming** | ❌ No | ✅ Yes |
| **Ranking** | ❌ No | ✅ Yes |
| **CPU Usage** | High | Low |
| **Scalability** | Poor | Excellent |

---

## 6. Search Query Examples

### 6.1 Simple Search
```python
# User input: "laptop"

query = {
    "query": {
        "match": {
            "nama": "laptop"
        }
    }
}

# Matches:
# - "Laptop Asus ROG"
# - "Laptop Gaming"
# - "Laptop Terbaik"
```

### 6.2 Multi-Field Search
```python
# User input: "laptop gaming"

query = {
    "query": {
        "multi_match": {
            "query": "laptop gaming",
            "fields": ["nama", "kategori", "spesifikasi"]
        }
    }
}

# Matches:
# - "Laptop Gaming Asus" (nama)
# - "Laptop" in kategori "Gaming Laptop" (kategori)
# - "Gaming Laptop" in spesifikasi (spesifikasi)
```

### 6.3 Filtered Search
```python
# User input: "laptop" with price filter

query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"nama": "laptop"}}
            ],
            "filter": [
                {"range": {"harga": {"lte": 10000000}}},
                {"range": {"stok": {"gt": 0}}}
            ]
        }
    }
}

# Matches:
# - "Laptop" in name
# - Price <= 10,000,000
# - Stock > 0 (available)
```

### 6.4 Phrase Search
```python
# User input: "laptop gaming"

query = {
    "query": {
        "match_phrase": {
            "nama": "laptop gaming"
        }
    }
}

# Matches:
# - "Laptop Gaming Asus" ✓
# - "Gaming Laptop Asus" ✗
```

### 6.5 Fuzzy Search
```python
# User input: "lapto" (typo)

query = {
    "query": {
        "fuzzy": {
            "nama": {
                "value": "lapto",
                "fuzziness": "AUTO"
            }
        }
    }
}

# Matches:
# - "laptop" (edit distance 1)
# - "lap top" (edit distance 2)
```

---

## 7. Search Response Format

### 7.1 Success Response
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

### 7.2 No Results Response
```json
{
  "status": "success",
  "message": "Ditemukan 0 hasil untuk 'xyz123'",
  "data": [],
  "total": 0,
  "keyword": "xyz123"
}
```

### 7.3 Error Response
```json
{
  "detail": "Elasticsearch tidak tersedia"
}
```

---

## 8. Frontend Search UI

### 8.1 Search Component
```vue
<!-- SearchBar.vue -->
<template>
  <div class="search-bar">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Cari produk..."
      @input="onSearchInput"
    />
    
    <div v-if="isSearching" class="spinner">
      Searching...
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const isSearching = ref(false)
const emit = defineEmits(['search-results'])

let debounceTimer = null

function onSearchInput() {
  // Clear previous timer
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // If query too short, clear results
  if (searchQuery.value.length < 2) {
    emit('search-results', [])
    return
  }
  
  // Debounce: wait 300ms
  debounceTimer = setTimeout(async () => {
    await performSearch(searchQuery.value)
  }, 300)
}

async function performSearch(query) {
  isSearching.value = true
  
  try {
    const response = await axios.get('http://localhost:8002/api/search', {
      params: { q: query }
    })
    
    emit('search-results', response.data)
  } catch (error) {
    console.error('Search failed:', error)
    emit('search-results', { data: [], total: 0 })
  } finally {
    isSearching.value = false
  }
}
</script>
```

### 8.2 Search Results Display
```vue
<!-- SearchResults.vue -->
<template>
  <div class="search-results">
    <div v-if="searchData.total > 0" class="results-header">
      Ditemukan {{ searchData.total }} hasil untuk "{{ searchData.keyword }}"
    </div>
    
    <div v-else-if="searchData.total === 0 && searchData.keyword" class="no-results">
      Tidak ditemukan hasil untuk "{{ searchData.keyword }}"
    </div>
    
    <div class="results-list">
      <ProductCard
        v-for="product in searchData.data"
        :key="product._id || product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  searchData: {
    type: Object,
    default: { data: [], total: 0, keyword: '' }
  }
})
</script>
```

---

## 9. Search Performance

### 9.1 Response Time Breakdown
```
User Input
    ↓
Debounce (300ms)
    ↓
Network (1-10ms)
    ↓
Search Service (5-10ms)
    ↓
Elasticsearch Query (10-50ms)
    ↓
Network (1-10ms)
    ↓
Frontend Rendering (10-50ms)
    ↓
Total: 330-430ms (including debounce)
```

### 9.2 Optimization Strategies

#### 1. Debouncing
```javascript
// Reduce unnecessary requests
// Wait for user to finish typing
setTimeout(async () => {
  await performSearch(query)
}, 300)
```

#### 2. Caching (Future)
```python
# Cache frequent searches
from redis import Redis

redis_client = Redis()

def cari_match(keyword: str):
    # Check cache first
    cached = redis_client.get(f"search:{keyword}")
    if cached:
        return json.loads(cached)
    
    # Search Elasticsearch
    results = es.search(keyword)
    
    # Cache for 5 minutes
    redis_client.setex(f"search:{keyword}", 300, json.dumps(results))
    
    return results
```

#### 3. Connection Pooling
```python
# Reuse Elasticsearch connections
from elasticsearch import Elasticsearch

# Create connection pool
client = Elasticsearch(
    ELASTIC_URI,
    maxsize=20,  # Connection pool size
    timeout=30
)
```

---

## 10. Search Analytics (Future)

### 10.1 Track Search Queries
```python
# Log search queries for analytics
@router.get("/search")
async def search_products(q: str):
    # Log search
    logger.info(f"Search query: {q}")
    
    # Track analytics
    analytics.track_search(q)
    
    # Execute search
    hasil = es.cari_match(q)
    
    return {
        "data": hasil,
        "total": len(hasil)
    }
```

### 10.2 Popular Searches
```python
# Get most searched keywords
@router.get("/search/trending")
async def get_trending_searches():
    trending = analytics.get_top_searches(limit=10)
    return {
        "trending": trending
    }
```

### 10.3 No Results Queries
```python
# Track queries with no results
# Helps identify missing products
@router.get("/search/analytics")
async def get_search_analytics():
    return {
        "total_searches": analytics.get_total_searches(),
        "no_results": analytics.get_no_results_queries(),
        "avg_response_time": analytics.get_avg_response_time()
    }
```

---

## 11. Why Not MongoDB for Search?

### 11.1 Limitations of MongoDB Search

#### Regex Search
```javascript
// MongoDB regex - slow!
db.products.find({
  $or: [
    {nama: {$regex: "laptop", $options: "i"}},
    {kategori: {$regex: "laptop", $options: "i"}}
  ]
})

// Problems:
// - Full collection scan
// - No relevance scoring
// - No fuzzy matching
// - Very slow for large datasets
```

#### Text Index (Better but still limited)
```javascript
// MongoDB text index
db.products.createIndex({
  nama: "text",
  kategori: "text",
  spesifikasi: "text"
})

// Search
db.products.find({
  $text: {$search: "laptop gaming"}
})

// Better than regex, but:
// - Limited scoring
// - No fuzzy matching
// - No advanced features
// - Still slower than Elasticsearch
```

### 11.2 Elasticsearch Advantages

| Feature | MongoDB | Elasticsearch |
|---------|---------|---------------|
| **Speed** | Slow (O(n)) | Fast (O(1)) |
| **Relevance Scoring** | Basic | Advanced (BM25) |
| **Fuzzy Matching** | ❌ | ✅ |
| **Stemming** | ❌ | ✅ |
| **Phonetic Search** | ❌ | ✅ |
| **Faceted Search** | Limited | Advanced |
| **Aggregations** | Basic | Advanced |
| **Scalability** | Limited | Excellent |
| **Real-time** | Yes | Near real-time |

### 11.3 When to Use MongoDB Search?
```
✅ Small dataset (< 1,000 documents)
✅ Simple exact match queries
✅ No need for relevance scoring
✅ Infrequent searches

❌ Large dataset
❌ Full-text search
❌ Need relevance ranking
❌ High search volume
```

### 11.4 When to Use Elasticsearch?
```
✅ Large dataset (> 10,000 documents)
✅ Full-text search required
✅ Need relevance scoring
✅ High search volume
✅ Complex queries
✅ Fuzzy matching needed
✅ Analytics required

This project: ✅ Use Elasticsearch
```

---

## Summary

### Search Flow
1. **User Input**: Type query in search box
2. **Debounce**: Wait 300ms for typing to stop
3. **API Call**: GET /api/search?q=query
4. **Query Analysis**: Tokenize query
5. **Index Lookup**: Find matching documents
6. **Scoring**: Calculate relevance scores
7. **Sorting**: Sort by score (highest first)
8. **Response**: Return top results
9. **Display**: Show results in UI

### Key Concepts
- **Inverted Index**: Fast lookup
- **Tokenization**: Break text into words
- **Stemming**: Normalize words
- **Relevance Scoring**: Rank results
- **Debouncing**: Reduce requests

### Performance
- **Response Time**: < 100ms
- **Debounce**: 300ms
- **Total UX Time**: ~400ms

### Why Elasticsearch?
- 10-100x faster than MongoDB regex
- Better relevance scoring
- Fuzzy matching
- Advanced features
- Scalable