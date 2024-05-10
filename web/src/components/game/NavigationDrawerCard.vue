<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ isHovering, props: activatorProps }"
  >
    <v-card
      v-if="entry.path"
      v-bind="activatorProps"
      class="grid-item"
      :disabled="isDisabled"
      flat
      @click="play"
      @keydown="play"
    >
      <img
        :src="entry.path"
        alt=""
        @error="onError"
      >

      <v-fade-transition>
        <v-container v-if="isHovering">
          <v-row
            justify="center"
            align="center"
          >
            <v-col cols="auto">
              <v-btn
                color="primary"
                size="large"
                icon="mdi-play"
                rounded="circle"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col
            class="pa-4"
            align="right"
          >
            <v-btn
              v-if="gameType === 'roi'"
              :title="$t('home.game_type.roi')"
              class="text-primary"
              size="small"
              icon="mdi-draw"
              density="comfortable"
              rounded="circle"
            />
            <v-btn
              v-else
              :title="$t('home.game_type.tagging')"
              class="text-primary"
              size="small"
              icon="mdi-tag-outline"
              density="comfortable"
              rounded="circle"
            />

            <v-btn
              v-if="opponentType === 'no_opponent'"
              :title="$t(`home.plugins.opponent_type.${opponentType}`)"
              class="ml-2 text-primary"
              size="small"
              density="comfortable"
              icon="mdi-account-off-outline"
              rounded="circle"
            />

            <v-btn
              v-if="tabooType && !tabooType.startsWith('no_')"
              :title="$t(`home.plugins.taboo_type.${tabooType}`)"
              class="ml-2 text-primary"
              size="small"
              density="comfortable"
              icon="mdi-filter-outline"
              rounded="circle"
            />

            <v-btn
              v-if="suggesterType && !suggesterType.startsWith('no_')"
              :title="$t(`home.plugins.suggester_type.${suggesterType}`)"
              class="ml-2 text-primary"
              size="small"
              density="comfortable"
              icon="mdi-lightbulb-variant-outline"
              rounded="circle"
            />
          </v-col>
        </v-row>

        <v-row />

        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <p v-if="title && title[i18n.global.locale.value]">
                {{ title[i18n.global.locale.value] }}
              </p>
              <!-- eslint-disable vue/no-v-html -->
              <p
                v-else
                v-html="$t(`home.fields.${entry.type}`, { value: entry.query })"
              />
              <!--eslint-enable-->
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-btn
      v-else
      border="secondary md opacity-100"
      color="secondary"
      variant="outlined"
      rounded
      block
      @click="play"
      @keydown="play"
    >
      <span class="text-primary-darken-1">
        <template v-if="title && title[i18n.global.locale.value]">
          {{ title[i18n.global.locale.value] }}
        </template>
        <template v-else>
          {{ $t("game.fields.newGameDefault") }}
        </template>
      </span>
    </v-btn>
  </v-hover>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'

const router = useRouter()
const store = useStore()

const isDisabled = ref(false)
function onError() {
  isDisabled.value = true
}

const props = defineProps({
  entry: {
    type: Object,
    default: null
  }
})
function play() {
  if (props.entry.params) {
    store.commit('game/updateDialog', { params: props.entry.params })
  }
  router.push({ name: 'game' })
}
const title = computed(() => props.entry.title)
const gameType = computed(() => props.entry.params.game_type)
const opponentType = computed(() => props.entry.params.opponent_type)
const tabooType = computed(() => props.entry.params.taboo_type)
const suggesterType = computed(() => props.entry.params.suggester_type)
</script>

<style scoped>
.v-container {
  flex-direction: column;
  position: absolute;
  display: flex;
  height: 100%;
  z-index: 99;
  width: 100%;
  bottom: 0;
  left: 0;
}

.v-container p {
  line-height: 1.25rem;
  margin-bottom: 0;
}

.v-container p::first-letter {
  text-transform: uppercase;
}

.v-container .overlay {
  background: linear-gradient(to top, black, #0000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #fff;
  height: 100%;
  left: 50%;
  top: 50%;
}
</style>
