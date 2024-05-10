<template>
  <div />
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import isArray from '@/composables/useIsArray'
import keyInObj from '@/composables/useKeyInObj'
import useMessage from '@/composables/useMessage'

const { t } = useI18n()

const props = defineProps({
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

const gameType = computed(() => props.params.game_type)
const tabooTags = computed(() => {
  if (keyInObj('taboo_tags', props.entry)) {
    return props.entry.taboo_tags.map(({ name }) => name)
  }
  return []
})
const opponentTags = computed(() => {
  if (keyInObj('opponent_tags', props.entry)) {
    return props.entry.opponent_tags.map(({ name }) => name)
  }
  return []
})

const tags = ref([])
onMounted(() => {
  tags.value.push({
    name: t(
      `game.fields.${gameType.value}.intro`
    ),
    created_after: 0
  })
  if (opponentTags.value.length) {
    tags.value.push({
      name: t(
        `game.fields.${gameType.value}.opponent`
      ),
      created_after: 0
    })
  } else {
    tags.value.push({
      name: t(
        `game.fields.${gameType.value}.noOpponent`,
      ),
      created_after: 0
    })
  }
  if (tabooTags.value.length) {
    tags.value.push({
      name: t(
        `game.fields.${gameType.value}.taboo`,
        { tags: tabooTags.value.join(', ') }
      ),
      created_after: 0,
      highlight: 1
    })
  }
  [0.5, 0.9].forEach((p) => {
    tags.value.push({
      name: t(
        'game.fields.basic.secondsLeft',
        { n: Math.floor((1 - p) * props.params.game_round_duration) },
      ),
      created_after: p * props.params.game_round_duration
    })
  })
})
onUnmounted(() => tags.value = [])

const filteredTags = computed(() => {
  if (isArray(tags.value)) {
    return tags.value.filter((tag) => (
      tag.created_after <= props.seconds
    ))
  }
  return []
})

const emit = defineEmits(['add'])
const { tagsToMessages } = useMessage(tags)
watch(filteredTags, (newTags, oldTags) => {
  const messages = tagsToMessages('default', newTags, oldTags)
  messages.forEach((message) => emit('add', message))
}, { immediate: true })
</script>
