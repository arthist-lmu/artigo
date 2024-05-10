<template>
  <v-snackbar
    v-model="display"
    class="mb-5"
    :timeout="-1"
    theme="dark"
    rounded
  >
    <span>{{ $t('search.fields.game') }}</span>

    <v-btn
      class="ml-4"
      size="small"
      rounded
      flat
      @click="goToGame()"
    >
      <span
        v-if="!mdAndDown"
        class="mr-1"
      >
        {{ $t('field.offWeGo') }}
      </span>

      <v-icon size="small">
        mdi-play
      </v-icon>
    </v-btn>
  </v-snackbar>
</template>

<script setup>
import { ref, computed, watch} from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'

const router = useRouter()
const store = useStore()
const { mdAndDown } = useDisplay()

function goToGame() {
  const params = {
    resource_inputs: searchData.value.map(({ resource_id }) => resource_id),
    resource_type: 'custom_resource'
  }
  store.commit('game/updateDialog', { params })
  router.push({ name: 'game' })
}

const display = ref(false)
const searchData = computed(() => store.state.search.data.entries)
watch(searchData, (values) => {
  if (values && values.length) {
    display.value = true
  }
})
</script>

<style scoped>
.v-overlay {
  z-index: 950 !important;
}
</style>
