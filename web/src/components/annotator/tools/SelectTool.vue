<template>
  <div />
</template>

<script setup>
import { watch } from 'vue'
import useTool from '@/composables/useTool'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const {
  tool,
  isActive,
  isDisabled
} = useTool(
  'select',
  props.modelValue
)

const emit = defineEmits([
  'setOffset',
  'update'
])

function onMouseDrag({ point, downPoint }) {
  emit('setOffset', point.subtract(downPoint))
}
tool.onMouseDrag = onMouseDrag

watch(isActive, (value) => {
  if (value) {
    tool.activate()
  }
}, { immediate: true })
watch(isDisabled, (value) => {
  if (value && isActive.value) {
    emit('update', null)
  }
})
</script>
