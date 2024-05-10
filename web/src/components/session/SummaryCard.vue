<template>
  <v-alert
    class="mb-0"
    type="surface-variant"
    density="comfortable"
  >
    <template #prepend>
      <v-progress-circular
        :size="48"
        :width="2"
        :rotate="-90"
        :model-value="progress"
        color="primary"
      >
        <span class="font-weight-medium">
          {{ value }}
        </span>
      </v-progress-circular>
    </template>

    <div :title="title">
      <div class="text-subtitle-1 text-black">
        {{ title }}
      </div>

      <div
        v-if="subvalue > 0"
        class="mt-n1 text-caption text-grey"
      >
        {{ subvalue.toFixed(2) }} {{ subtitle }}
      </div>
    </div>
  </v-alert>
</template>

<script setup>
import { ref, nextTick } from 'vue'

defineProps({
  icon: {
    type: String,
    default: null
  },
  title: {
    type: String,
    default: null
  },
  subtitle: {
    type: String,
    default: null
  },
  value: {
    type: Number,
    default: 0
  },
  subvalue: {
    type: Number,
    default: 0
  }
})

const progress = ref(0)
setTimeout(() => {
  nextTick(() => {
    progress.value = 100
  })
}, 250)
</script>

<style scoped>
.v-alert .v-progress-circular {
  background-color: transparent;
  border-radius: 24px;
  transition: background-color 0.25s linear;
}

.v-alert:hover .v-progress-circular {
  background-color: rgba(66 71 152 15%);
}
</style>
