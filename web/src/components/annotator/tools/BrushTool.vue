<template>
  <div />
</template>

<script setup>
import { watch } from 'vue'
import paper from 'paper'
import useTool from '@/composables/useTool'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  bounds: {
    type: Object,
    required: true
  }
})

const {
  tool,
  getRoi,
  isActive,
  isDisabled
} = useTool(
  'brush',
  props.modelValue
)

const emit = defineEmits([
  'setOffset',
  'update',
  'export'
])

let path = null
function createPath() {
  return new paper.Path({
    strokeColor: 'rgba(66, 71, 152, 0.5)',
    strokeWidth: 25,
    strokeCap: 'round'
  })
}
function removePath() {
  if (path) {
    path.removeSegments()
  }
}
function createPoint({ x, y }) {
  const {
    xMin, xMax, yMin, yMax
  } = props.bounds
  if (x < xMin) {
    x = xMin
  } else if (x > xMax) {
    x = xMax
  }
  if (y < yMin) {
    y = yMin
  } else if (y > yMax) {
    y = yMax
  }
  return new paper.Point(x, y)
}

function onMouseDown({ event, point }) {
  if (!event.ctrlKey) {
    removePath()
    path = createPath()
    path.add(createPoint(point))
  }
}
function onMouseDrag({ event, point, downPoint }) {
  if (event.ctrlKey) {
    const offset = point.subtract(downPoint)
    emit('setOffset', offset)
  } else {
    path.add(createPoint(point))
    path.smooth()
  }
}
function onMouseUp({ event, point }) {
  if (!event.ctrlKey) {
    path.add(createPoint(point))
    path.smooth()
    const { strokeBounds } = path
    removePath()
    path = new paper.Path.Rectangle({
      rectangle: strokeBounds,
      fillColor: 'rgba(66, 71, 152, 0.5)',
      selected: true
    })
    const roi = getRoi(
      strokeBounds,
      props.bounds,
      true
    )
    emit('export', roi)
  }
}
tool.onMouseDown = onMouseDown
tool.onMouseDrag = onMouseDrag
tool.onMouseUp = onMouseUp

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
