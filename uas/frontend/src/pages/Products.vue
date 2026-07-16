<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="mb-1">
          <i class="bi bi-box me-2 text-primary"></i>Daftar Produk
        </h4>
        <p class="text-muted mb-0 small">Kelola data produk toko komputer</p>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-success" @click="handleSeed" :disabled="seedLoading">
          <span v-if="seedLoading" class="spinner-border spinner-border-sm me-1"></span>
          <i v-else class="bi bi-database-fill-up me-1"></i>Seed Data
        </button>
        <button class="btn btn-primary" @click="openAddModal">
          <i class="bi bi-plus-circle me-1"></i>Tambah Produk
        </button>
      </div>
    </div>

    <!-- Loading -->
    <Loading v-if="loading" message="Memuat daftar produk..." />

    <!-- Error -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
    </div>

    <!-- Table -->
    <div v-else class="card border-0 shadow-sm">
      <div class="card-body p-0">
        <ProductTable
          :products="products"
          @edit="openEditModal"
          @delete="confirmDelete"
        />
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <ProductModal
      ref="productModal"
      modal-id="productModal"
      :is-edit="isEdit"
      :product="selectedProduct"
      :loading="submitLoading"
      @submit="handleSubmit"
    />

    <!-- Delete Confirmation -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="bi bi-exclamation-triangle me-2"></i>Konfirmasi Hapus
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p class="mb-0">
              Yakin ingin menghapus produk <strong>{{ deleteTarget?.nama }}</strong> (ID: {{ deleteTarget?._id }})?
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              <i class="bi bi-x-circle me-1"></i>Batal
            </button>
            <button type="button" class="btn btn-danger" @click="handleDelete" :disabled="deleteLoading">
              <span v-if="deleteLoading" class="spinner-border spinner-border-sm me-1"></span>
              <i v-else class="bi bi-trash me-1"></i>Hapus
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1080;">
      <div v-if="toast.show" class="toast show" :class="`bg-${toast.type}`" role="alert">
        <div class="toast-header text-white" :class="`bg-${toast.type}`">
          <i :class="['bi me-2', toast.type === 'success' ? 'bi-check-circle' : 'bi-exclamation-circle']"></i>
          <strong class="me-auto">{{ toast.title }}</strong>
          <button type="button" class="btn-close btn-close-white" @click="toast.show = false"></button>
        </div>
        <div class="toast-body text-white">
          {{ toast.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Modal } from 'bootstrap'
import Loading from '../components/Loading.vue'
import ProductTable from '../components/ProductTable.vue'
import ProductModal from '../components/ProductModal.vue'
import {
  getAllProducts,
  createProduct,
  updateProduct,
  deleteProduct,
  seedProducts
} from '../services/api'

const products = ref([])
const loading = ref(true)
const error = ref('')

// Modal state
const productModal = ref(null)
const isEdit = ref(false)
const selectedProduct = ref(null)
const submitLoading = ref(false)

// Delete state
const deleteModal = ref(null)
const deleteTarget = ref(null)
const deleteLoading = ref(false)

// Seed state
const seedLoading = ref(false)

// Toast
const toast = reactive({
  show: false,
  type: 'success',
  title: '',
  message: ''
})

function showToast(type, title, message) {
  toast.type = type
  toast.title = title
  toast.message = message
  toast.show = true
  setTimeout(() => { toast.show = false }, 4000)
}

async function loadProducts() {
  loading.value = true
  error.value = ''
  try {
    const res = await getAllProducts()
    products.value = res.data.data || []
  } catch (e) {
    const msg = e.response?.data?.detail || 'Gagal memuat produk'
    error.value = msg
  } finally {
    loading.value = false
  }
}

function openAddModal() {
  isEdit.value = false
  selectedProduct.value = null
  if (productModal.value) productModal.value.show()
}

function openEditModal(product) {
  isEdit.value = true
  selectedProduct.value = { ...product }
  if (productModal.value) productModal.value.show()
}

async function handleSubmit(formData) {
  submitLoading.value = true
  try {
    if (isEdit.value) {
      const { _id, ...data } = formData
      await updateProduct(_id, data)
      showToast('success', 'Berhasil', 'Produk berhasil diupdate')
    } else {
      await createProduct(formData)
      showToast('success', 'Berhasil', 'Produk berhasil ditambahkan')
    }
    if (productModal.value) productModal.value.hide()
    await loadProducts()
  } catch (e) {
    const msg = e.response?.data?.detail || 'Gagal menyimpan produk'
    showToast('danger', 'Gagal', msg)
  } finally {
    submitLoading.value = false
  }
}

function confirmDelete(product) {
  deleteTarget.value = product
  const modalEl = document.getElementById('deleteModal')
  if (modalEl) {
    const modal = new Modal(modalEl)
    modal.show()
  }
}

async function handleDelete() {
  if (!deleteTarget.value) return
  deleteLoading.value = true
  try {
    await deleteProduct(deleteTarget.value._id)
    showToast('success', 'Berhasil', 'Produk berhasil dihapus')
    const modalEl = document.getElementById('deleteModal')
    if (modalEl) {
      const modal = Modal.getInstance(modalEl)
      if (modal) modal.hide()
    }
    await loadProducts()
  } catch (e) {
    const msg = e.response?.data?.detail || 'Gagal menghapus produk'
    showToast('danger', 'Gagal', msg)
  } finally {
    deleteLoading.value = false
    deleteTarget.value = null
  }
}

async function handleSeed() {
  seedLoading.value = true
  try {
    const res = await seedProducts()
    showToast('success', 'Berhasil', res.data.message || 'Data berhasil di-seed')
    await loadProducts()
  } catch (e) {
    const msg = e.response?.data?.detail || 'Gagal seed data'
    showToast('danger', 'Gagal', msg)
  } finally {
    seedLoading.value = false
  }
}

onMounted(() => {
  loadProducts()
})
</script>