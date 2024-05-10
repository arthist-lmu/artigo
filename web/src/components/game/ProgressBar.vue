<template>
  <v-progress-linear
    :model-value="progress"
    :color="progress >= 85 ? 'error' : 'primary'"
  />
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  params: {
    type: Object,
    default: null
  }
})

const seconds = ref(0)
const duration = computed(() => props.params.game_round_duration)
const progress = computed(() => (seconds.value / duration.value) * 100)

const emit = defineEmits(['progress', 'next'])
emit('progress', seconds.value)
const timer = setInterval(() => {
  if (seconds.value === duration.value) {
    emit('next')
  } else {
    seconds.value += 1
    emit('progress', seconds.value)
  }
}, 1000)

onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.v-progress-linear {
  position: absolute;
  z-index: 4;
}
</style>
