<template>
  <div class="container py-4">
    <div class="text-center mb-4">
      <h4 class="mb-1">
        <i class="bi bi-search me-2 text-primary"></i>Pencarian Produk
      </h4>
      <p class="text-muted mb-0 small">
        Cari produk menggunakan full-text search Elasticsearch
      </p>
    </div>

    <!-- Search Bar -->
    <div class="mb-4">
      <SearchBar
        v-model="keyword"
        :disabled="searchLoading"
        @search="handleSearch"
      />
    </div>

    <!-- Loading -->
    <Loading v-if="searchLoading" message="Mencari data..." />

    <!-- Error -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
    </div>

    <!-- Hasil Pencarian -->
    <div v-else-if="hasSearched">
      <!-- Info hasil -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <p class="mb-0 text-muted">
          <i class="bi bi-info-circle me-1"></i>
          Menampilkan <strong>{{ results.length }}</strong> hasil untuk
          <strong>"{{ lastKeyword }}"</strong>
        </p>
      </div>

      <!-- Empty State -->
      <div v-if="results.length === 0" class="text-center py-5">
        <i class="bi bi-emoji-frown fs-1 text-muted d-block mb-3"></i>
        <h5 class="text-muted">Tidak ditemukan</h5>
        <p class="text-muted small">
          Tidak ada produk yang cocok dengan "{{ lastKeyword }}"
        </p>
      </div>

      <!-- Cards Grid -->
      <div v-else class="row g-4">
        <div v-for="product in results" :key="product._id" class="col-md-6 col-lg-4">
          <SearchCard :product="product" />
        </div>
      </div>
    </div>

    <!-- Initial State -->
    <div v-else class="text-center py-5">
      <i class="bi bi-arrow-up-circle fs-1 text-primary d-block mb-3"></i>
      <h5 class="text-muted">Mulai Pencarian</h5>
      <p class="text-muted small">
        Ketik kata kunci di atas, lalu tekan Enter atau klik tombol Cari.
        <br />
        Contoh: laptop, keyboard, mouse, monitor, ssd
      </p>
      <div class="d-flex justify-content-center gap-2 mt-3">
        <button
          v-for="sample in samples"
          :key="sample"
          class="btn btn-outline-primary btn-sm"
          @click="quickSearch(sample)"
        >
          {{ sample }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SearchBar from '../components/SearchBar.vue'
import SearchCard from '../components/SearchCard.vue'
import Loading from '../components/Loading.vue'
import { searchProducts } from '../services/api'

const keyword = ref('')
const lastKeyword = ref('')
const results = ref([])
const searchLoading = ref(false)
const hasSearched = ref(false)
const error = ref('')

const samples = ['laptop', 'keyboard', 'mouse', 'monitor', 'ssd']

async function handleSearch() {
  const q = keyword.value.trim()
  if (!q) return

  searchLoading.value = true
  error.value = ''
  hasSearched.value = true
  lastKeyword.value = q

  try {
    const res = await searchProducts(q)
    results.value = res.data.data || []
  } catch (e) {
    if (e.response?.status === 503) {
      error.value = 'Search Service tidak tersedia. Pastikan Elasticsearch sudah berjalan.'
    } else {
      error.value = e.response?.data?.detail || 'Gagal melakukan pencarian'
    }
    results.value = []
  } finally {
    searchLoading.value = false
  }
}

function quickSearch(sample) {
  keyword.value = sample
  handleSearch()
}
</script>