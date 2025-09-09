<template>
  <div
    v-if="isLoading"
    class="loading"
  >
    <v-progress-circular
      color="error"
      indeterminate
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const isLoading = computed(() => store.state.utils.status.loading)
</script>

<style scoped>
.loading {
  background-color: rgb(0 0 0 / 30%);
  text-align: center;
  position: fixed;
  z-index: 999;
  inset: 0;
}

.loading > div {
  height: 100% !important;
}
</style>
