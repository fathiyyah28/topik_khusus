import axios from 'axios'

const CORE_SERVICE_URL = import.meta.env.VITE_CORE_SERVICE_URL || 'http://localhost:8001/api'
const SEARCH_SERVICE_URL = import.meta.env.VITE_SEARCH_SERVICE_URL || 'http://localhost:8002/api'

const coreApi = axios.create({
  baseURL: CORE_SERVICE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

const searchApi = axios.create({
  baseURL: SEARCH_SERVICE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// =====================
// Product API (Core Service)
// =====================

export function getAllProducts() {
  return coreApi.get('/products')
}

export function getProductById(id) {
  return coreApi.get(`/products/${id}`)
}

export function createProduct(product) {
  return coreApi.post('/products', product)
}

export function updateProduct(id, data) {
  return coreApi.put(`/products/${id}`, data)
}

export function deleteProduct(id) {
  return coreApi.delete(`/products/${id}`)
}

export function seedProducts() {
  return coreApi.post('/products/seed')
}

// =====================
// Search API (Search Service)
// =====================

export function searchProducts(query) {
  return searchApi.get('/search', { params: { q: query } })
}

export function getSearchStats() {
  return searchApi.get('/stats')
}

// =====================
// Health / Status
// =====================

export function checkCoreService() {
  return coreApi.get('/products', { timeout: 3000 })
}

export function checkSearchService() {
  return searchApi.get('/stats', { timeout: 3000 })
}

export default {
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
  seedProducts,
  searchProducts,
  getSearchStats,
  checkCoreService,
  checkSearchService
}