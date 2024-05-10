<template>
  <div />
</template>

<script setup>
import { watch, computed } from 'vue'
import isArray from '@/composables/useIsArray'
import useMessage from '@/composables/useMessage'

const props = defineProps({
  entry: {
    type: Object,
    default: null
  },
  seconds: {
    type: Number,
    default: 0
  }
})

const tags = computed(() => props.entry.opponent_tags)

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
  const messages = tagsToMessages('opponent', newTags, oldTags)
  messages.forEach((message) => emit('add', message))
})
</script>
