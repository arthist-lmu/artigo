<template>
  <v-app-bar
    :style="getStyle"
    :height="height"
    class="search mt-0"
    style="position: fixed;"
    order="2"
    flat
  >
    <v-container class="mt-4">
      <v-row>
        <v-col class="pb-0">
          <slot>
            <DefaultSearchBar
              :store-name="storeName"
              :filter="filter"
            />
          </slot>
        </v-col>
      </v-row>

      <slot name="append-item" />
    </v-container>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import DefaultSearchBar from '@/components/utils/DefaultSearchBar.vue'

defineProps({
  storeName: {
    type: String,
    required: true
  },
  height: {
    type: Number,
    required: false,
    default: 114
  },
  filter: {
    type: Boolean,
    required: false
  }
})

const getStyle = computed(() => {
  const header = document.querySelector('header')
  return {
    'margin-top': `${header.offsetHeight}px`
  }
})
</script>

<style scoped>
.row.aggregate + .row.aggregate {
  margin-top: 0;
}
</style>
