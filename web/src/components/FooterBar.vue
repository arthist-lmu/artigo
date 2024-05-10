<template>
  <v-footer
    v-if="isVisible"
    style="position: fixed;"
    order="1"
    app
  >
    <v-container
      :class="{
        'px-7': smAndDown,
        opaque: opaque
      }"
      class="py-1"
    >
      <v-row>
        <v-col
          :cols="mdAndDown ? '4' : '6'"
          align-self="center"
        >
          <v-btn
            :title="$t('about.title')"
            :size="mdAndDown ? 'x-small' : 'small'"
            color="primary"
            rounded
            flat
            @click="goTo('about')"
          >
            <v-icon class="mr-2">
              mdi-information-outline
            </v-icon>

            2010–{{ new Date().getFullYear() }}
          </v-btn>

          <v-chip
            v-if="!mdAndDown"
            class="ml-2"
            variant="text"
            size="small"
            flat
            @click="goTo('institute')"
          >
            {{ $t('institute.title') }}
          </v-chip>
        </v-col>

        <v-col
          :cols="mdAndDown ? '8' : '6'"
          align-self="center"
          align="right"
        >
          <v-btn
            v-if="!mdAndDown"
            :href="apiHref"
            target="_blank"
            rel="noopener noreferrer"
            :size="mdAndDown ? 'small' : 'default'"
            density="comfortable"
            icon="mdi-api"
            flat
          />

          <v-btn
            v-for="page in pages"
            :key="page"
            class="ml-2"
            :size="mdAndDown ? 'x-small' : 'small'"
            border="secondary md opacity-100"
            color="secondary"
            variant="outlined"
            rounded
            @click="goTo(page)"
          >
            <span class="text-primary-darken-1">
              {{ $t(`${page}.title`) }}
            </span>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import goTo from '@/composables/useGoTo'

const route = useRoute()
const store = useStore()

defineProps({
  opaque: {
    type: Boolean,
    default: false
  }
})

const {
  smAndUp,
  mdAndDown
} = useDisplay()

const pages = [
  'imprint',
  'privacyPolicy'
]

const apiHref = computed(() => {
  let baseURL = 'http://localhost:8000'
  const { VUE_APP_API } = import.meta.env
  if (VUE_APP_API) {
    baseURL = `https://${VUE_APP_API}`
  }
  return `${baseURL}/schema/redoc`
})
const isVisible = computed(() => {
  if (
    route.name !== 'game'
    || smAndUp
  ) {
    return true
  }
  return store.state.game.input.focus
})
</script>

<style scoped>
.v-footer > .v-container {
  transition: opacity .5s ease-out;
}

.v-footer > .v-container.opaque {
  opacity: 0.25;
}

.v-footer .v-container:hover {
  opacity: 1;
}
</style>
