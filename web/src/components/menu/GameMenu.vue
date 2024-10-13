<template>
  <v-btn
    :title="$t('game.title')"
    class="play"
    color="primary"
    variant="text"
    density="compact"
    icon="mdi-play"
    flat
    @click="goToGame()"
  />
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'

const route = useRoute()
const router = useRouter()
const store = useStore()

function goToGame() {
  const params = {}
  if (route.name === 'search') {
    params.resource_inputs = store.state.search.data.map(({ resource_id }) => resource_id)
    params.resource_type = 'custom_resource'
  }
  store.commit('game/updateDialog', { params })
  if (route.name === 'game') {
    router.go(0)
  } else {
    router.push({ name: 'game' })
  }
}
</script>

<style scoped>
.play {
  position: absolute;
  width: 44px !important;
  left: 152px;
  top: 2px;
}

.play,
.play::before {
  border-radius: 12px;
}
</style>
