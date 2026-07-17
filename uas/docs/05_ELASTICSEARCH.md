# ELASTICSEARCH

## Apa itu Search Engine?

### Definisi
Search Engine adalah sistem yang dirancang untuk mencari dan mengorganisir informasi dalam large datasets dengan cepat dan efisien. Search engine modern menggunakan sophisticated algorithms untuk indexing, ranking, dan retrieving data.

### Perbedaan Database vs Search Engine

| Aspek | Database (MongoDB) | Search Engine (Elasticsearch) |
|-------|-------------------|-------------------------------|
| **Primary Purpose** | CRUD operations | Full-text search & analytics |
| **Query Type** | Exact match, regex | Full-text, fuzzy, semantic |
| **Performance** | Good untuk structured queries | Excellent untuk text search |
| **Indexing** | B-tree indexes | Inverted indexes |
| **Scoring** | No relevance scoring | BM25, TF-IDF scoring |
| **Use Case** | Transactional data | Search, log analytics, monitoring |

### Kapan Menggunakan Search Engine?
✅ Full-text search dibutuhkan  
✅ Relevance ranking penting  
✅ Fuzzy matching diperlukan  
✅ Large-scale text data  
✅ Real-time analytics  
✅ Log aggregation  
✅ Application monitoring  
✅ Autocomplete & suggestions  

---

## Apa itu Full-Text Search?

### Definisi
Full-text search adalah teknik untuk mencari text dalam large text corpus dengan understanding dari text content, bukan hanya exact matching.

### Fitur Full-Text Search

#### 1. Tokenization
Memecah text menjadi individual words (tokens):
```
Input: "Laptop Gaming Terbaik"
Tokens: ["laptop", "gaming", "terbaik"]
```

#### 2. Normalization
- Lowercase: "Laptop" → "laptop"
- Remove punctuation: "laptop!" → "laptop"
- Remove stopwords: "the", "is", "di", "ke"

#### 3. Stemming
Mengembalikan kata ke bentuk dasar:
```
"gaming" → "game"
"running" → "run"
"makanan" → "makan"
```

#### 4. Lemmatization
Similar dengan stemming tapi menggunakan dictionary:
```
"better" → "good" (bukan "bet")
"mice" → "mouse" (bukan "mic")
```

#### 5. Fuzzy Matching
Toleransi terhadap typo:
```
Query: "lapto"
Matches: "laptop" (distance 1)
```

#### 6. Phrase Search
Search exact phrase:
```
Query: "laptop gaming"
Matches documents containing both words in sequence
```

#### 7. Proximity Search
Search words within certain distance:
```
Query: "laptop gaming"~5
Matches documents where "laptop" and "gaming" are within 5 words
```

---

## Konsep Dasar Elasticsearch

### 1. Index

#### Definisi
Index adalah container untuk documents yang memiliki similar characteristics. Setara dengan database di SQL.

#### Properties
- **Mapping**: Schema definition untuk documents
- **Settings**: Configuration (number of shards, replicas)
- **Analyzers**: Text processing rules
- **Aliases**: Alternative names untuk index

#### Example
```json
{
  "produk": {
    "mappings": {
      "properties": {
        "nama": {"type": "text"},
        "harga": {"type": "integer"}
      }
    },
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1
    }
  }
}
```

### 2. Document

#### Definisi
Document adalah unit dasar data di Elasticsearch. Format JSON.

#### Structure
```json
{
  "_id": 1,
  "_source": {
    "nama": "Laptop Asus",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15
  }
}
```

#### Metadata Fields
- `_id`: Unique identifier
- `_index`: Index name
- `_score`: Relevance score
- `_source`: Original document

### 3. Mapping

#### Definisi
Mapping adalah schema definition untuk index yang defines:
- Field names dan types
- How fields should be indexed
- How text should be analyzed

#### Example
```json
{
  "mappings": {
    "properties": {
      "nama": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "harga": {
        "type": "integer"
      },
      "tags": {
        "type": "keyword"
      }
    }
  }
}
```

#### Data Types
- **text**: Full-text search (analyzed)
- **keyword**: Exact match (not analyzed)
- **integer**: Integer numbers
- **float**: Floating point numbers
- **boolean**: true/false
- **date**: Dates
- **object**: Nested objects
- **nested**: Array of objects

### 4. Analyzer

#### Definisi
Analyzer adalah komponen yang mengubah text menjadi tokens untuk indexing.

#### Components

##### Character Filters
Pre-processing sebelum tokenization:
- HTML strip: Remove HTML tags
- Mapping: Character replacement
- Pattern replace: Regex replacement

##### Tokenizer
Memecah text menjadi tokens:
- **standard**: Default tokenizer (letter-based)
- **whitespace**: Split by whitespace
- **letter**: Split on non-letters
- **lowercase**: Convert to lowercase
- **uax_url_email**: Special handling untuk URLs dan emails

##### Token Filters
Post-processing setelah tokenization:
- **lowercase**: Convert to lowercase
- **stop**: Remove stopwords (the, is, di, ke)
- **stemmer**: Stemming (gaming → game)
- **synonym**: Synonym replacement
- **asciifolding**: Remove accents (café → cafe)

#### Built-in Analyzers
```json
{
  "analyzer": "standard",  // Default
  "analyzer": "simple",    // Non-letter split
  "analyzer": "whitespace", // Whitespace split
  "analyzer": "language",  // Language-specific (english, indonesian)
  "analyzer": "custom"     // Custom analyzer
}
```

#### Custom Analyzer Example
```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom",
          "char_filter": ["html_strip"],
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "stemmer"]
        }
      }
    }
  }
}
```

### 5. Token

#### Definisi
Token adalah unit kecil dari text setelah proses analysis.

#### Example
```
Input: "Laptop Gaming Terbaik!"
    ↓
Character Filter (lowercase): "laptop gaming terbaik!"
    ↓
Tokenizer: ["laptop", "gaming", "terbaik"]
    ↓
Token Filter (stopwords): ["laptop", "gaming"]  // "terbaik" removed if stopword
    ↓
Final Tokens: ["laptop", "gaming"]
```

#### Token Attributes
- **term**: The token text
- **position**: Position in the text
- **start_offset**: Start character offset
- **end_offset**: End character offset
- **type**: Token type (<ALPHANUM>, <NUM>, etc.)

### 6. Inverted Index

#### Definisi
Inverted Index adalah data structure yang mapping token → documents. Ini adalah rahasia mengapa Elasticsearch sangat cepat.

#### Structure
```
Token      → Document IDs
"laptop"   → [1, 5, 12, 23, 45]
"gaming"   → [5, 12, 23]
"asus"     → [1, 12]
"terbaik"  → [5, 12, 23, 45]
```

#### Bagaimana Ini Bekerja?

**Traditional Database (Full Scan):**
```
Query: "laptop"
    ↓
Scan ALL documents
    ↓
Check each document if contains "laptop"
    ↓
Return matches
Time: O(n) - Linear time
```

**Elasticsearch (Inverted Index):**
```
Query: "laptop"
    ↓
Lookup "laptop" in inverted index
    ↓
Get document IDs: [1, 5, 12, 23, 45]
    ↓
Return documents
Time: O(1) - Constant time
```

#### Keuntungan
✅ **Fast Lookup**: Langsung akses document IDs  
✅ **Scalable**: Performance tetap cepat meskipun data bertambah  
✅ **Memory Efficient**: Hanya store tokens, bukan full documents  
✅ **Multi-term Queries**: Mudah untuk AND, OR, NOT operations  

### 7. Relevance Score

#### Definisi
Relevance score adalah nilai yang menunjukkan seberapa cocok document dengan query. Document dengan score lebih tinggi dianggap lebih relevan.

#### Scoring Algorithms

##### TF-IDF (Term Frequency - Inverse Document Frequency)
```
TF (Term Frequency) = Frekuensi term dalam document
IDF (Inverse Document Frequency) = log(total_docs / docs_with_term)
Score = TF × IDF
```

**Example:**
```
Document 1: "laptop gaming laptop" (2x "laptop")
Document 2: "laptop terbaik" (1x "laptop")
Total docs: 100
Docs with "laptop": 50

TF-IDF for "laptop" in Doc 1:
TF = 2
IDF = log(100/50) = log(2) = 0.301
Score = 2 × 0.301 = 0.602

TF-IDF for "laptop" in Doc 2:
TF = 1
IDF = log(100/50) = 0.301
Score = 1 × 0.301 = 0.301
```

Doc 1 lebih relevan karena score lebih tinggi.

##### BM25 (Best Match 25)
Default scoring algorithm di Elasticsearch. Improvement dari TF-IDF:
- **Saturation**: TF di-cap untuk prevent domination oleh frequent terms
- **Length normalization**: Adjust score berdasarkan document length
- **Better for short queries**: More accurate untuk short queries

#### Score Range
- Score > 1.0: Very relevant
- Score 0.5 - 1.0: Relevant
- Score 0.1 - 0.5: Somewhat relevant
- Score < 0.1: Less relevant

### 8. Cluster, Node, Shard, Replica

#### Cluster
- Group of nodes yang bekerja sama
- Single cluster = single search engine
- Cluster name harus unique
- Default cluster name: "elasticsearch"

#### Node
- Single instance dari Elasticsearch
- Part of a cluster
- Stores data dan participates in indexing dan search
- Types:
  - **Master Node**: Manages cluster metadata
  - **Data Node**: Stores data dan executes CRUD
  - **Ingest Node**: Pre-processes documents
  - **Coordinating Node**: Routes requests

#### Shard
- Partition dari index
- Allows horizontal scaling
- Primary shard: Original shard
- Types:
  - **Primary Shard**: Original copy
  - **Replica Shard**: Copy dari primary shard

#### Replica
- Copy dari primary shard
- Provides high availability
- Can serve search requests
- Default: 1 replica per shard

#### Example
```
Index: "produk"
  ├─ Shard 0 (Primary)    → Node 1
  │   └─ Replica 0        → Node 2
  ├─ Shard 1 (Primary)    → Node 2
  │   └─ Replica 1        → Node 3
  └─ Shard 2 (Primary)    → Node 3
      └─ Replica 2        → Node 1

Total: 3 primary shards + 3 replicas = 6 shards
```

---

## Bagaimana Proses Search?

### Step-by-Step Process

```
User Query: "laptop gaming"
    ↓
┌─────────────────────────────────────────┐
│ STEP 1: Query Analysis                  │
│ "laptop gaming" → ["laptop", "gaming"]  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ STEP 2: Lookup Inverted Index           │
│ "laptop" → [1, 5, 12, 23, 45]          │
│ "gaming" → [5, 12, 23]                 │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ STEP 3: Merge Results (AND operation)   │
│ Intersection: [5, 12, 23]               │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ STEP 4: Calculate Scores                │
│ Doc 5:  TF(laptop)=2, TF(gaming)=1      │
│         Score = 2.45                     │
│ Doc 12: TF(laptop)=1, TF(gaming)=1      │
│         Score = 1.89                     │
│ Doc 23: TF(laptop)=1, TF(gaming)=1      │
│         Score = 1.23                     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ STEP 5: Sort by Score                   │
│ [Doc 5 (2.45), Doc 12 (1.89), Doc 23]  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ STEP 6: Return Results                  │
│ Top N documents sorted by relevance     │
└─────────────────────────────────────────┘
```

### Diagram Search Flow

```
┌──────────┐
│  User    │
│  Query:  │
│ "laptop" │
└────┬─────┘
     │
     ▼
┌──────────────────┐
│ Query Analyzer   │
│ "laptop"         │
│ → ["laptop"]     │
└────┬─────────────┘
     │
     ▼
┌──────────────────────────┐
│ Inverted Index Lookup    │
│ "laptop" → [1,5,12,23]   │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Fetch Documents          │
│ Get docs 1,5,12,23       │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Calculate Scores         │
│ Doc 1: 0.85              │
│ Doc 5: 2.45 ← Highest    │
│ Doc 12: 1.89             │
│ Doc 23: 1.23             │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Sort by Score            │
│ [Doc 5, Doc 12, Doc 23]  │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Return Top N Results     │
└──────────────────────────┘
```

---

## Query DSL (Domain Specific Language)

### Match Query
Full-text search dengan relevance scoring:
```json
{
  "query": {
    "match": {
      "nama": "laptop gaming"
    }
  }
}
```

### Multi-Match Query
Search di multiple fields:
```json
{
  "query": {
    "multi_match": {
      "query": "laptop gaming",
      "fields": ["nama", "kategori", "spesifikasi"],
      "type": "best_fields"
    }
  }
}
```

### Match Phrase
Exact phrase matching:
```json
{
  "query": {
    "match_phrase": {
      "nama": "laptop gaming"
    }
  }
}
```

### Bool Query
Combine multiple queries:
```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"nama": "laptop"}}
      ],
      "should": [
        {"match": {"kategori": "gaming"}}
      ],
      "must_not": [
        {"match": {"stok": 0}}
      ],
      "filter": [
        {"range": {"harga": {"lte": 10000000}}}
      ]
    }
  }
}
```

### Term Query
Exact match (no analysis):
```json
{
  "query": {
    "term": {
      "kategori": "Laptop"
    }
  }
}
```

### Range Query
Range filtering:
```json
{
  "query": {
    "range": {
      "harga": {
        "gte": 5000000,
        "lte": 20000000
      }
    }
  }
}
```

### Fuzzy Query
Fuzzy matching dengan edit distance:
```json
{
  "query": {
    "fuzzy": {
      "nama": {
        "value": "lapto",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

---

## Kelebihan Elasticsearch

✅ **Full-Text Search**: Pencarian text yang advanced  
✅ **Relevance Scoring**: Hasil diurutkan berdasarkan relevansi  
✅ **Fuzzy Matching**: Toleransi terhadap typo  
✅ **Multi-Field Search**: Search di multiple fields sekaligus  
✅ **Faceted Search**: Filtering dan aggregation  
✅ **Horizontal Scalability**: Distributed architecture  
✅ **Real-Time Search**: Near real-time indexing (1 second default)  
✅ **Rich Query DSL**: Powerful query language  
✅ **Analytics**: Built-in analytics capabilities  
✅ **High Availability**: Replication dan failover  
✅ **Auto-Completion**: Suggest dan autocomplete features  
✅ **Geo-Search**: Location-based search  

---

## Kekurangan Elasticsearch

❌ **Complex Setup**: Memerlukan understanding yang dalam  
❌ **Memory Intensive**: High RAM usage untuk large indices  
❌ **Steep Learning Curve**: Query DSL dan concepts kompleks  
❌ **Operational Complexity**: Sharding, replication, cluster management  
❌ **Not for Transactions**: Tidak support ACID transactions  
❌ **Eventual Consistency**: Bukan instant consistency  
❌ **Overkill untuk Small Data**: Tidak cocok untuk datasets kecil  
❌ **Resource Heavy**: CPU dan memory hungry  
❌ **No Multi-Document ACID**: Tidak ada atomic operations across documents  

---

## Elasticsearch dalam Project Ini

### Role
- **Search Engine**: Full-text search untuk produk
- **Analytics**: Search analytics (optional)
- **Real-time Indexing**: Sync dengan MongoDB

### Index Configuration
```json
{
  "mappings": {
    "properties": {
      "nama": {
        "type": "text",
        "analyzer": "standard"
      },
      "kategori": {
        "type": "text",
        "analyzer": "standard"
      },
      "harga": {
        "type": "integer"
      },
      "stok": {
        "type": "integer"
      },
      "spesifikasi": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}
```

### Operations in Project

#### Index Document
```python
client.index(
  index="produk",
  id=doc_id,
  body={
    "nama": "Laptop Asus",
    "kategori": "Laptop",
    "harga": 18999000,
    "stok": 15,
    "spesifikasi": "AMD Ryzen 9, RAM 16GB"
  }
)
```

#### Search
```python
query = {
  "query": {
    "multi_match": {
      "query": "laptop gaming",
      "fields": ["nama", "kategori", "spesifikasi"],
      "type": "best_fields"
    }
  }
}

response = client.search(index="produk", body=query)
results = [hit["_source"] for hit in response["hits"]["hits"]]
```

#### Update
```python
client.update(
  index="produk",
  id=product_id,
  body={"doc": {"harga": 20000000}}
)
```

#### Delete
```python
client.delete(
  index="produk",
  id=product_id
)
```

### Performance
- **Indexing**: < 10ms per document
- **Search**: < 100ms untuk 1 million documents
- **Throughput**: 1000+ queries/second

---

## Elasticsearch Commands Reference

### Index Management
```bash
# Create index
PUT /produk

# Delete index
DELETE /produk

# List indices
GET /_cat/indices?v

# Index stats
GET /produk/_stats

# Health check
GET /_cluster/health
```

### Document Operations
```bash
# Index document
POST /produk/_doc/1
{
  "nama": "Laptop Asus",
  "harga": 18999000
}

# Get document
GET /produk/_doc/1

# Update document
POST /produk/_doc/1/_update
{
  "doc": {"harga": 20000000}
}

# Delete document
DELETE /produk/_doc/1

# Bulk operations
POST /_bulk
{ "index": { "_index": "produk", "_id": "1" } }
{ "nama": "Laptop", "harga": 5000000 }
{ "index": { "_index": "produk", "_id": "2" } }
{ "nama": "Phone", "harga": 3000000 }
```

### Search Operations
```bash
# Search all
GET /produk/_search
{
  "query": {"match_all": {}}
}

# Full-text search
GET /produk/_search
{
  "query": {
    "match": {
      "nama": "laptop gaming"
    }
  }
}

# Multi-field search
GET /produk/_search
{
  "query": {
    "multi_match": {
      "query": "laptop",
      "fields": ["nama", "kategori", "spesifikasi"]
    }
  }
}

# Filtered search
GET /produk/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"nama": "laptop"}}
      ],
      "filter": [
        {"range": {"harga": {"lte": 10000000}}}
      ]
    }
  }
}
```

### Aggregation
```bash
# Terms aggregation
GET /produk/_search
{
  "aggs": {
    "kategori_count": {
      "terms": {"field": "kategori"}
    }
  }
}

# Average aggregation
GET /produk/_search
{
  "aggs": {
    "avg_harga": {
      "avg": {"field": "harga"}
    }
  }
}