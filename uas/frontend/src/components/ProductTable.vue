<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
      <thead class="table-primary">
        <tr>
          <th scope="col" class="text-center" style="width: 60px;">ID</th>
          <th scope="col">Nama</th>
          <th scope="col">Kategori</th>
          <th scope="col" class="text-end">Harga</th>
          <th scope="col" class="text-center">Stok</th>
          <th scope="col">Spesifikasi</th>
          <th scope="col" class="text-center" style="width: 160px;">Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="products.length === 0">
          <td colspan="7" class="text-center text-muted py-4">
            <i class="bi bi-inbox fs-3 d-block mb-2"></i>
            Belum ada data produk. Silakan seed data terlebih dahulu.
          </td>
        </tr>
        <tr v-for="product in products" :key="product._id">
          <td class="text-center fw-bold">{{ product._id }}</td>
          <td>{{ product.nama }}</td>
          <td><span class="badge bg-info">{{ product.kategori }}</span></td>
          <td class="text-end fw-semibold text-success">{{ formatHarga(product.harga) }}</td>
          <td class="text-center">
            <span :class="stokBadge(product.stok)">{{ product.stok }}</span>
          </td>
          <td class="text-truncate" style="max-width: 200px;">{{ product.spesifikasi }}</td>
          <td class="text-center">
            <button class="btn btn-sm btn-outline-primary me-1" @click="$emit('edit', product)">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" @click="$emit('delete', product)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  products: {
    type: Array,
    default: () => []
  }
})

defineEmits(['edit', 'delete'])

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