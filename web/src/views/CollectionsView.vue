<template>
  <v-container :style="entries && entries.length ? undefined : 'height: 100%;'">
    <SearchBar
      store-name="collections"
      :height="112"
    >
      <template #append-item>
        <div style="height: 12px;" />
      </template>
    </SearchBar>

    <DataIterator
      :component="component"
      store-name="collections"
      :reload="true"
    />
  </v-container>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import DataIterator from '@/components/utils/DataIterator.vue'
import SearchBar from'@/components/utils/ExtendedSearchBar.vue'
import SearchResultCard from '@/components/collection/SearchResultCard.vue'

const store = useStore()

const component = computed(() => SearchResultCard)
const entries = computed(() => store.state.collections.data.entries)
</script>

<style scoped>
.v-container > div {
  height: 100%;
}

.v-row > .v-col:empty {
  display: none;
}
</style>
