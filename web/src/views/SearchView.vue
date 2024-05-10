<template>
  <v-container :style="entries && entries.length ? undefined : 'height: 100%;'">
    <SearchBar
      store-name="search"
      :height="height"
      :filter="true"
    >
      <template #append-item>
        <v-row
          v-for="aggregation in aggregations"
          :key="aggregation.field"
          class="aggregate"
        >
          <v-col v-if="aggregation.entries.length">
            <v-slide-group show-arrows>
              <v-slide-item
                v-for="item in aggregation.entries"
                :key="item.name"
              >
                <v-chip
                  class="mx-1"
                  border="secondary md opacity-100"
                  variant="outlined"
                  rounded
                  @click="search(item.name)"
                >
                  {{ item.name }}
                </v-chip>
              </v-slide-item>
            </v-slide-group>
          </v-col>
        </v-row>
      </template>
    </SearchBar>

    <v-data-iterator
      :class="mdAndDown ? 'px-3' : 'px-2'"
      :items="entries || []"
      :items-per-page="itemsPerPage"
      hide-default-footer
    >
      <template #default="{ items }">
        <v-row>
          <v-col
            v-for="item in items"
            :key="item.raw.resource_id"
            :cols="(12 / itemsPerRow)"
            class="pa-1"
          >
            <SearchResultCard :item="item.raw" />
          </v-col>
        </v-row>
      </template>

      <template #no-data>
        <v-row
          v-if="entries && entries.length == 0"
          justify="center"
        >
          <v-col
            :cols="noDataCols"
            align-self="center"
          >
            <v-alert
              type="error"
              icon="mdi-alert-circle-outline"
            >
              {{ $t('search.fields.noResults') }}
            </v-alert>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>

    <ToasterBar />
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import useDisplayItems from '@/composables/useDisplayItems'
import ToasterBar from '@/components/search/ToasterBar.vue'
import SearchBar from '@/components/utils/ExtendedSearchBar.vue'
import SearchResultCard from '@/components/search/SearchResultCard.vue'

const route = useRoute()
const store = useStore()
const { mdAndDown } = useDisplay()

const entries = computed(() => store.state.search.data.entries)

const {
  itemsPerPage,
  itemsPerRow,
  noDataCols
} = useDisplayItems('search')

function search(value) {
  const query = { tags: value }
  store.dispatch('search/post', { query })
}

const aggregations = computed(() => store.state.search.data.aggregations)
const height = computed(() => {
  let height = 100
  if (aggregations.value.length) {
    aggregations.value.forEach((aggregation) => {
      if (aggregation.entries.length) {
        height += 56
      }
    })
  }
  return height
})

onMounted(() => {
  store.dispatch('search/getURLParams', route.query)
  window.onpopstate = () => {
    store.commit('search/toggleBackBtn')
    store.dispatch('search/getURLParams', route.query)
  }
})
</script>

<style>
.v-data-iterator > div:not(.v-row) {
  height: 100%;
}
</style>

<style scoped>
.v-container > div,
.v-container .justify-center {
  height: 100%;
}

.v-row > .v-col:empty {
  display: none;
}
</style>
