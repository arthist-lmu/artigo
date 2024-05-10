<template>
  <div class="loading">
    <v-hover v-slot="{ isHovering, props: activatorProps }">
      <div v-bind="activatorProps">
        <v-btn
          v-if="paused"
          color="primary"
          size="x-large"
          icon="mdi-play"
          @click="togglePause"
        />
        <template v-else>
          <v-btn
            v-if="isHovering"
            color="primary"
            size="x-large"
            icon="mdi-pause"
            @click="togglePause"
          />
          <v-btn
            v-else
            :color="duration - seconds < 1 ? 'error' : 'primary'"
            size="x-large"
            icon
          >
            {{ duration - seconds }}
          </v-btn>
        </template>
      </div>
    </v-hover>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const props = defineProps({
  params: {
    type: Object,
    default: null
  },
  duration: {
    type: Number,
    default: 3
  }
})

const paused = ref(false)
function togglePause() {
  paused.value = !paused.value
}

const seconds = ref(0)
const emit = defineEmits(['finish'])
const timer = setInterval(() => {
  if (!paused.value) {
    if (seconds.value === props.duration) {
      emit('finish')
    } else {
      seconds.value += 1
    }
  }
}, 1000)
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
