<template>
  <v-container>
    <v-row>
      <v-col class="text-center">
        <span class="text-caption text-grey">
          {{ $t("game.fields.basic.rounds", { i: roundId, total: rounds }) }}
        </span>

        <v-btn
          v-if="roundId <= rounds"
          :title="$t('game.fields.basic.skip')"
          class="ml-2"
          color="grey"
          size="x-small"
          variant="text"
          density="comfortable"
          icon="mdi-chevron-right"
          @click="next"
        />

        <v-btn
          :title="$t('game.fields.basic.finish')"
          color="grey"
          size="x-small"
          variant="text"
          density="comfortable"
          icon="mdi-page-last"
          @click="finish"
        />
      </v-col>
    </v-row>

    <v-row v-if="highlights && highlights.length">
      <v-col>
        <transition-group name="fade">
          <template v-for="(message, i) in highlights">
            <DefaultMessage
              v-if="message.from === 'default'"
              :key="i"
              :message="message"
            />
          </template>
        </transition-group>
      </v-col>
    </v-row>

    <v-row
      ref="container"
      class="mt-3 pb-0 align-end"
    >
      <v-col class="pt-0">
        <slot name="messages">
          <MessagesTemplate
            :entry="entry"
            :params="params"
            :seconds="seconds"
            @update="scroll"
          />
        </slot>
      </v-col>
    </v-row>

    <slot name="append-item" />
  </v-container>
</template>

<script setup>
import { ref, nextTick, computed, watch } from 'vue'
import { useStore } from 'vuex'
import MessagesTemplate from './messages/MessagesTemplate.vue'
import DefaultMessage from './messages/DefaultMessage.vue'

const store = useStore()

defineProps({
  entry: {
    type: Object,
    default: null
  },
  params: {
    type: Object,
    default: null
  },
  seconds: {
    type: Number,
    default: 0
  }
})

const focus = ref(false)
watch(focus, (value) => {
  store.commit('game/updateInput', { focus: value })
})

const container = ref()
const highlights = ref([])
const currentScrollTop = ref(0)
function isMessageOutOfViewport(message) {
  const element = container.value.$el.querySelector(`#highlight-${message.highlight}`)
  if (element) {
    const { bottom } = element.getBoundingClientRect()
    const { top } = container.value.$el.getBoundingClientRect()
    return bottom - 25 <= top
  }
  return false
}
function scroll({ from, messages }) {
  // only scroll down if the user has not scrolled up
  if (container.value === undefined) return null
  const { scrollHeight, scrollTop } = container.value.$el
  if (from === 'user' || scrollTop + 50 >= currentScrollTop.value) {
    nextTick(() => {
      container.value.$el.scrollTop = scrollHeight
      currentScrollTop.value = container.value.$el.scrollTop
    })
  }
  // highlight messages that are outside the viewport
  const shouldHighlight = (message) => {
    return !highlights.value.some(({ text }) => text === message.text) && isMessageOutOfViewport(message)
  }
  messages.forEach((message) => {
    if (shouldHighlight(message)) {
      highlights.value.push(message)
    }
  })
}

const emit = defineEmits([
  'next',
  'finish'
])
function next() {
  emit('next')
}
function finish() {
  emit('finish')
}

const roundId = computed(() => store.state.game.roundId)
const rounds = computed(() => store.state.game.rounds)
</script>

<style scoped>
.v-container {
  flex-direction: column;
  display: flex;
}

.v-row:not(.align-end) {
  flex: 0;
}

.v-row.align-end {
  overflow-y: auto;
  margin-right: 0;
  height: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 1s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
