<template>
  <v-data-iterator
    class="px-2"
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
          <component
            :is="component"
            :item="item.raw"
          />
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
            {{ $t(`${storeName}.fields.noResults`) }}
          </v-alert>
        </v-col>
      </v-row>
    </template>
  </v-data-iterator>
</template>

<script setup>
import { computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import useDisplayItems from '@/composables/useDisplayItems'

const store = useStore()

const props = defineProps({
  component: {
    type: Object,
    required: true
  },
  storeName: {
    type: String,
    required: true
  },
  reload: {
    type: Boolean,
    default: false
  }
})

const entries = computed(() => store.state[props.storeName].data.entries)

const {
  itemsPerPage,
  itemsPerRow,
  noDataCols
} = useDisplayItems(props.storeName)

let checkInterval = null
function setReload() {
  if (checkInterval === null) {
    checkInterval = setInterval(() => {
      store.dispatch(`${props.storeName}/post`, {})
    }, 10 * 1000)
  }
}
function removeReload() {
  clearInterval(checkInterval)
  checkInterval = null
}
watch(props.reload, (value) => {
  if (value) {
    setReload()
  } else {
    removeReload()
  }
}, { immediate: true })

let observer = null
onMounted(() => {
  observer = new MutationObserver(() => {
    const overlay = document.querySelector('.v-overlay')
    if (overlay !== null) {
      removeReload()
    } else {
      setReload()
    }
  })
  const app = document.querySelector('#app')
  observer.observe(app, {
    childList: true
  })
  window.scrollTo(0, 0)
})
onBeforeUnmount(() => {
  observer.disconnect()
  removeReload()
})

store.dispatch(`${props.storeName}/post`, {})
</script>

<style>
.v-data-iterator > div:not(.v-row),
.v-data-iterator > div > .v-row {
  height: 100%;
}
</style>
