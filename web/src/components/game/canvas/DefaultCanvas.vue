<template>
  <div
    ref="container"
    style="position: relative;"
  >
    <slot name="prepend-item" />

    <CanvasTemplate
      :key="key"
      :src="entry.path"
      :tool="tool"
      class="bg-grey-lighten-2"
      :height="height"
      contain
      @load="onLoad"
      @error="onError"
      @update="onUpdate"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import CanvasTemplate from '@/components/annotator/CanvasTemplate.vue'

const props = defineProps({
  tool: {
    type: String,
    default: 'select'
  },
  entry: {
    type: Object,
    default: null
  },
  params: {
    type: Object,
    default: null
  }
})

const key = computed(() => `${props.entry.path}-${height.value}`)

const container = ref()
const height = ref(0)
function setHeight() {
  if (container.value !== undefined) {
    height.value = container.value.offsetHeight
  }
}

watch(() => props.entry.path, () => setHeight())
onMounted(() => setHeight())
onUnmounted(() => window.removeEventListener('resize', setHeight))

const emit = defineEmits([
  'load',
  'error',
  'update'
])
function onLoad() {
  emit('load')
}
function onError() {
  emit('error')
}
function onUpdate(values) {
  emit('update', values)
}

window.addEventListener('resize', setHeight)
</script>
