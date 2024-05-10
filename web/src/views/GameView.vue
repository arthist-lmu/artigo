<template>
  <v-container
    :class="[mdAndDown ? 'mobile px-1' : undefined, 'mt-8']"
    style="position: relative; height: calc(100% - 36px);"
  >
    <template v-if="!dialog.inital">
      <CountdownTemplate
        v-if="countdown"
        :duration="3"
        @finish="finishGameround"
      />
      <v-card
        v-else
        style="overflow: clip;"
        color="surface-variant"
        flat
      >
        <ProgressBar
          v-if="!loading"
          :params="params"
          @next="next"
          @progress="progress"
        />

        <v-row class="pb-0">
          <v-col
            class="py-0"
            :cols="mdAndDown ? 12 : 8"
          >
            <ROICanvas
              v-if="gameType === 'roi'"
              tool="brush"
              :entry="entry"
              :params="params"
              @load="onLoad"
              @error="next"
            />
            <DefaultCanvas
              v-else
              :entry="entry"
              :params="params"
              @load="onLoad"
              @error="next"
            />
          </v-col>

          <v-col
            v-if="!loading"
            class="py-0"
            :cols="mdAndDown ? 12 : 4"
          >
            <TaggingSidebar
              v-if="gameType === 'tagging'"
              :key="path"
              :entry="entry"
              :params="params"
              :seconds="seconds"
              @next="next"
              @finish="finishGamesession"
            />
            <DefaultSidebar
              v-else
              :key="path"
              :entry="entry"
              :params="params"
              :seconds="seconds"
              @next="next"
              @finish="finishGamesession"
            />
          </v-col>
        </v-row>
      </v-card>
    </template>
    
    <SelectDialog v-model="dialog.inital" />

    <v-dialog
      v-model="dialog.helper"
      style="z-index: 9999 !important;"
      max-width="400"
    >
      <HelperCard
        v-model="dialog.helper"
        :text="$t('game.helper')"
        icon="mdi-help-circle-outline"
        page="about"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, nextTick, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import ProgressBar from '@/components/game/ProgressBar.vue'
import CountdownTemplate from '@/components/game/CountdownTemplate.vue'
import DefaultCanvas from '@/components/game/canvas/DefaultCanvas.vue'
import ROICanvas from '@/components/game/canvas/ROICanvas.vue'
import DefaultSidebar from '@/components/game/sidebar/DefaultSidebar.vue'
import TaggingSidebar from '@/components/game/sidebar/TaggingSidebar.vue'
import SelectDialog from '@/components/game/SelectDialog.vue'
import HelperCard from '@/components/HelperCard.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()

const { mdAndDown } = useDisplay()

const dialog = ref({
  initial: true,
  helper: false
})
function get() {
  dialog.value.inital = true
}
watch('$route.params.lang', () => {
  get()
})
onBeforeRouteUpdate(() => {
  get()
})

watch(() => dialog.value.inital, (value) => {
  if (value) {
    if (localStorage.getItem('gameHelper') === null) {
      localStorage.setItem('gameHelper', true)
      dialog.value.helper = true
    }
    loading.value = true
  }
})

const path = ref(null)
function onLoad() {
  if (!store.state.utils.status.loading) {
    path.value = entry.value.path
  }
}
watch(path, () => {
  nextTick(() => {
    loading.value = false
  })
})

onMounted(() => {
  store.dispatch('game/getURLParams', route.query)
  window.onpopstate = () => {
    store.dispatch('game/getURLParams', route.query)
    loading.value = true
  }
  nextTick(() =>
    get()
  )
})

const countdown = ref(false)
const loading = ref(true)
function next() {
  if (roundId.value === rounds.value) {
    finishGamesession()
  } else {
    countdown.value = true
    loading.value = true
  }
}
function finishGameround() {
  store.dispatch('game/get', {}).then(() => {
    countdown.value = false
  })
}
function finishGamesession() {
  const { sessionId: id } = store.state.game
  router.push({ name: 'session', params: { id } })
}
onBeforeRouteLeave((to, from, next) => {
  loading.value = true
  nextTick(() => {
    next()
  })
})

const seconds = ref(0)
function progress(value) {
  seconds.value = value
}

const entry = computed(() => store.state.game.entry)
const params = computed(() => store.state.game.params)
const roundId = computed(() => store.state.game.roundId)
const rounds = computed(() => store.state.game.rounds)
const gameType = computed(() => params.value.game_type)
</script>

<style scoped>
.v-container div:not([role='progressbar']) {
  height: 100%;
}

.v-container.mobile .v-row {
  height: 50%;
}
</style>
