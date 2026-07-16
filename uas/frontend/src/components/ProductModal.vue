<template>
  <div class="modal fade" :id="modalId" tabindex="-1" aria-hidden="true" ref="modal">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">
            <i :class="isEdit ? 'bi bi-pencil-square' : 'bi bi-plus-circle'" class="me-2"></i>
            {{ isEdit ? 'Edit Produk' : 'Tambah Produk' }}
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">ID Produk</label>
                <input
                  type="number"
                  class="form-control"
                  v-model.number="form._id"
                  :disabled="isEdit"
                  min="1"
                  required
                />
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Nama Produk</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="form.nama"
                  placeholder="Masukkan nama produk"
                  required
                />
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label fw-semibold">Kategori</label>
                <select class="form-select" v-model="form.kategori" required>
                  <option value="" disabled>Pilih kategori</option>
                  <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
                </select>
              </div>
              <div class="col-md-3 mb-3">
                <label class="form-label fw-semibold">Harga (Rp)</label>
                <input
                  type="number"
                  class="form-control"
                  v-model.number="form.harga"
                  placeholder="0"
                  min="0"
                  required
                />
              </div>
              <div class="col-md-3 mb-3">
                <label class="form-label fw-semibold">Stok</label>
                <input
                  type="number"
                  class="form-control"
                  v-model.number="form.stok"
                  placeholder="0"
                  min="0"
                  required
                />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Spesifikasi</label>
              <textarea
                class="form-control"
                v-model="form.spesifikasi"
                rows="2"
                placeholder="Masukkan spesifikasi produk"
                required
              ></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
            <i class="bi bi-x-circle me-1"></i>Batal
          </button>
          <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
            <i v-else :class="isEdit ? 'bi bi-save' : 'bi bi-plus-circle'" class="me-1"></i>
            {{ isEdit ? 'Simpan Perubahan' : 'Tambah Produk' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  modalId: {
    type: String,
    default: 'productModal'
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  product: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const categories = [
  'Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Flashdisk',
  'SSD', 'RAM', 'Printer', 'Webcam', 'Speaker', 'Harddisk', 'Router'
]

const form = reactive({
  _id: null,
  nama: '',
  kategori: '',
  harga: 0,
  stok: 0,
  spesifikasi: ''
})

const modal = ref(null)
let bsModal = null

onMounted(() => {
  if (modal.value) {
    bsModal = new Modal(modal.value)
  }
})

watch(() => props.product, (val) => {
  if (val) {
    form._id = val._id
    form.nama = val.nama
    form.kategori = val.kategori
    form.harga = val.harga
    form.stok = val.stok
    form.spesifikasi = val.spesifikasi
  } else {
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  form._id = null
  form.nama = ''
  form.kategori = ''
  form.harga = 0
  form.stok = 0
  form.spesifikasi = ''
}

function handleSubmit() {
  emit('submit', { ...form })
}

function show() {
  if (bsModal) bsModal.show()
}

function hide() {
  if (bsModal) bsModal.hide()
}

defineExpose({ show, hide })
</script>