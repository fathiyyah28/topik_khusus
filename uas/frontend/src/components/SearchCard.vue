<template>
  <div class="card h-100 shadow-sm border-0">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title mb-0 text-primary">{{ product.nama }}</h5>
        <span class="badge bg-info fs-6">{{ product.kategori }}</span>
      </div>
      <hr class="my-2" />
      <div class="row mb-2">
        <div class="col-6">
          <small class="text-muted d-block">
            <i class="bi bi-currency-exchange me-1"></i>Harga
          </small>
          <strong class="text-success">{{ formatHarga(product.harga) }}</strong>
        </div>
        <div class="col-6">
          <small class="text-muted d-block">
            <i class="bi bi-box-seam me-1"></i>Stok
          </small>
          <span :class="stokBadge(product.stok)">{{ product.stok }} unit</span>
        </div>
      </div>
      <div>
        <small class="text-muted d-block">
          <i class="bi bi-info-circle me-1"></i>Spesifikasi
        </small>
        <p class="card-text mb-0 small text-secondary">{{ product.spesifikasi }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  }
})

function formatHarga(harga) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(harga)
}

function stokBadge(stok) {
  if (stok <= 0) return 'badge bg-danger'
  if (stok <= 10) return 'badge bg-warning text-dark'
  return 'badge bg-success'
}
</script>