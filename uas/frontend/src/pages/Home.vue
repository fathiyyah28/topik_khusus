<template>
  <div class="container py-5">
    <!-- Hero -->
    <div class="text-center mb-5">
      <div class="display-1 text-primary mb-3">
        <i class="bi bi-search-heart"></i>
      </div>
      <h1 class="display-5 fw-bold">Mongo Search Portal</h1>
      <p class="lead text-muted mx-auto" style="max-width: 600px;">
        Aplikasi demonstrasi perbandingan pencarian data antara 
        <strong>MongoDB</strong> (regex) dan <strong>Elasticsearch</strong> (full-text search)
        dengan studi kasus Toko Peralatan Komputer.
      </p>
    </div>

    <!-- Architecture -->
    <div class="row justify-content-center mb-5">
      <div class="col-lg-10">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-center p-4">
            <h5 class="card-title text-primary mb-3">
              <i class="bi bi-diagram-3 me-2"></i>Arsitektur Sistem
            </h5>
            <div class="d-flex justify-content-center align-items-center flex-wrap gap-3">
              <div class="p-3 bg-light rounded">
                <i class="bi bi-window fs-2 text-info d-block mb-2"></i>
                <small class="fw-semibold">Vue.js</small>
              </div>
              <i class="bi bi-arrow-right fs-4 text-muted d-none d-sm-block"></i>
              <div class="p-3 bg-light rounded">
                <i class="bi bi-server fs-2 text-primary d-block mb-2"></i>
                <small class="fw-semibold">Core Service</small>
                <br />
                <small class="text-muted">FastAPI + MongoDB</small>
              </div>
              <i class="bi bi-arrow-right fs-4 text-muted d-none d-sm-block"></i>
              <div class="p-3 bg-light rounded">
                <i class="bi bi-server fs-2 text-success d-block mb-2"></i>
                <small class="fw-semibold">Search Service</small>
                <br />
                <small class="text-muted">FastAPI + ES</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row g-4">
      <div class="col-md-3 col-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-box-seam fs-1 text-primary mb-2"></i>
            <h3 class="fw-bold mb-0">{{ stats.totalProducts }}</h3>
            <small class="text-muted">Total Produk</small>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-database fs-1" :class="stats.mongoStatus ? 'text-success' : 'text-danger'"></i>
            <h3 class="fw-bold mb-0">
              <span v-if="stats.mongoStatus === null" class="text-warning">
                <i class="bi bi-hourglass-split"></i>
              </span>
              <span v-else-if="stats.mongoStatus" class="text-success">
                <i class="bi bi-check-circle"></i>
              </span>
              <span v-else class="text-danger">
                <i class="bi bi-x-circle"></i>
              </span>
            </h3>
            <small class="text-muted">MongoDB</small>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-search fs-1" :class="stats.esStatus ? 'text-success' : 'text-danger'"></i>
            <h3 class="fw-bold mb-0">
              <span v-if="stats.esStatus === null" class="text-warning">
                <i class="bi bi-hourglass-split"></i>
              </span>
              <span v-else-if="stats.esStatus" class="text-success">
                <i class="bi bi-check-circle"></i>
              </span>
              <span v-else class="text-danger">
                <i class="bi bi-x-circle"></i>
              </span>
            </h3>
            <small class="text-muted">Elasticsearch</small>
          </div>
        </div>
      </div>
      <div class="col-md-3 col-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body text-center p-4">
            <i class="bi bi-server fs-1" :class="stats.searchServiceStatus ? 'text-success' : 'text-danger'"></i>
            <h3 class="fw-bold mb-0">
              <span v-if="stats.searchServiceStatus === null" class="text-warning">
                <i class="bi bi-hourglass-split"></i>
              </span>
              <span v-else-if="stats.searchServiceStatus" class="text-success">
                <i class="bi bi-check-circle"></i>
              </span>
              <span v-else class="text-danger">
                <i class="bi bi-x-circle"></i>
              </span>
            </h3>
            <small class="text-muted">Search Service</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-warning mt-4">
      <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { getAllProducts, checkCoreService, checkSearchService } from '../services/api'

const stats = reactive({
  totalProducts: 0,
  mongoStatus: null,
  esStatus: null,
  searchServiceStatus: null
})

const error = ref('')

async function loadStats() {
  // Cek Core Service
  try {
    const res = await getAllProducts()
    stats.totalProducts = res.data.total || 0
    stats.mongoStatus = true
  } catch {
    stats.mongoStatus = false
  }

  // Cek Search Service
  try {
    const res = await checkSearchService()
    stats.searchServiceStatus = true
    if (res.data.data && res.data.data.status === 'connected') {
      stats.esStatus = true
    } else if (res.data.data && res.data.data.status === 'no_index') {
      stats.esStatus = true // ES running but no index yet
    } else {
      stats.esStatus = false
    }
  } catch {
    stats.searchServiceStatus = false
    stats.esStatus = false
  }
}

import { ref } from 'vue'

onMounted(() => {
  loadStats().catch(e => {
    error.value = 'Gagal memuat status sistem. Pastikan backend sudah berjalan.'
  })
})
</script>