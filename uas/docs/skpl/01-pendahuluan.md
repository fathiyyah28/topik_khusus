# BAB 1: PENDAHULUAN

## 1.1 Latar Belakang

Perkembangan teknologi informasi mendorong kebutuhan akan sistem pencarian data yang cepat, akurat, dan efisien. Dua teknologi basis data yang populer digunakan adalah MongoDB (basis data NoSQL berbasis dokumen) dan Elasticsearch (mesin pencarian full-text). Masing-masing memiliki kelebihan dan kekurangan dalam menangani pencarian data.

MongoDB unggul dalam pencarian eksak dan query terstruktur menggunakan regex, sedangkan Elasticsearch unggul dalam pencarian full-text berkat penggunaan inverted index. Perbandingan performa antara keduanya menjadi topik yang menarik untuk dikaji, khususnya dalam konteks aplikasi toko peralatan komputer.

Proyek ini bertujuan untuk membangun aplikasi berbasis microservice yang mendemonstrasikan perbandingan pencarian data antara MongoDB dan Elasticsearch. Aplikasi dikembangkan dengan arsitektur modern menggunakan FastAPI sebagai backend, Vue.js 3 sebagai frontend, serta Docker untuk containerization.

## 1.2 Tujuan

Tujuan dari pengembangan perangkat lunak ini adalah:

1. Membangun aplikasi berbasis microservice dengan dua service backend (Core Service dan Search Service).
2. Mengimplementasikan CRUD (Create, Read, Update, Delete) data produk menggunakan MongoDB.
3. Mengimplementasikan full-text search menggunakan Elasticsearch.
4. Menyediakan REST API yang terdokumentasi dengan Swagger.
5. Menyediakan antarmuka web yang responsif dan mudah digunakan.
6. Mengemas seluruh aplikasi dalam container Docker untuk kemudahan deployment.

## 1.3 Ruang Lingkup

Ruang lingkup proyek ini meliputi:

1. **Core Service**: Layanan backend untuk operasi CRUD data produk pada MongoDB.
2. **Search Service**: Layanan backend untuk full-text search pada Elasticsearch.
3. **Frontend Web**: Antarmuka pengguna berbasis Vue.js 3 dengan tiga halaman (Home, Products, Search).
4. **REST API**: Antarmuka komunikasi antar service dan antara frontend dengan backend.
5. **Docker**: Containerization untuk seluruh komponen aplikasi.
6. **Dataset**: 12 produk toko peralatan komputer sebagai data demonstrasi.

## 1.4 Definisi dan Singkatan

| Istilah/Singkatan | Definisi |
|-------------------|----------|
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| Docker | Platform containerization untuk mengemas aplikasi |
| Elasticsearch | Mesin pencarian full-text berbasis Lucene |
| FastAPI | Framework Python untuk membangun REST API |
| MongoDB | Basis data NoSQL berbasis dokumen |
| REST | Representational State Transfer |
| SKPL | Spesifikasi Kebutuhan Perangkat Lunak |
| Vue.js | Framework JavaScript untuk membangun antarmuka pengguna |

## 1.5 Referensi

1. FastAPI Documentation. https://fastapi.tiangolo.com/
2. Vue.js 3 Documentation. https://vuejs.org/
3. MongoDB Documentation. https://www.mongodb.com/docs/
4. Elasticsearch Documentation. https://www.elastic.co/guide/
5. Docker Documentation. https://docs.docker.com/
6. Bootstrap 5 Documentation. https://getbootstrap.com/docs/5.3/