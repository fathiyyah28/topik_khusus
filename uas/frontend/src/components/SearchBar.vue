<template>
  <div class="search-bar-container">
    <div class="input-group input-group-lg">
      <span class="input-group-text bg-white border-end-0">
        <i class="bi bi-search text-primary"></i>
      </span>
      <input
        type="text"
        class="form-control border-start-0 ps-0"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        @keyup.enter="$emit('search')"
        placeholder="Cari produk... (contoh: laptop, keyboard, mouse)"
        aria-label="Search"
      />
      <button
        v-if="modelValue"
        class="btn btn-outline-secondary"
        @click="$emit('update:modelValue', '')"
      >
        <i class="bi bi-x-lg"></i>
      </button>
      <button class="btn btn-primary" @click="$emit('search')" :disabled="disabled">
        <i class="bi bi-search me-1"></i>Cari
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue', 'search'])
</script>

<style scoped>
.search-bar-container {
  max-width: 700px;
  margin: 0 auto;
}
</style>