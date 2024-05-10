<template>
  <div />
</template>

<script setup>
import { watch, computed } from 'vue'
import { useStore } from 'vuex'
import useMessage from '@/composables/useMessage'

const store = useStore()

const tags = computed(() => store.state.game.tags)

const emit = defineEmits(['add'])
const {
  filteredTags,
  tagsToMessages
} = useMessage(tags)
watch(filteredTags, (newTags, oldTags) => {
  const messages = tagsToMessages('user', newTags, oldTags)
  messages.forEach((message) => emit('add', message))
}, { deep: true })
</script>
