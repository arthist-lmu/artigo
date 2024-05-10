<template>
  <v-dialog
    v-model="dialog"
    :retain-focus="false"
    max-width="750"
    scrollable
  >
    <ResourceCard
      v-if="resourceData"
      :key="resourceData.id"
      :item="resourceData"
      @close="dialog = false;"
    />
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import ResourceCard from '@/components/ResourceCard.vue'

const route = useRoute()
const store = useStore()

const resourceData = computed(() => store.state.resource.data)
watch(resourceData, (value) => {
  if (value) {
    dialog.value = true
  }
})

const dialog = ref(false)
watch(dialog, (value) => {
  if (!value) {
    store.commit('resource/updateData', null)
  }
})
watch(route, () => dialog.value = false)
</script>
