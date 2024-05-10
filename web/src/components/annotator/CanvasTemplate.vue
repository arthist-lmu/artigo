<template>
  <v-img
    class="image-wrapper"
    alt=""
    @load="onLoad"
    @error="onError"
  >
    <template #placeholder>
      <slot name="placeholder" />
    </template>

    <v-avatar
      v-if="avatarText"
      class="ma-4"
      color="primary"
      size="44"
    >
      <span class="white--text">
        {{ avatarText }}
      </span>
    </v-avatar>

    <div
      class="canvas-container"
      @wheel.prevent="onWheel"
    >
      <div v-if="activeTool">
        <SelectTool
          v-model="activeTool"
          @set-offset="setOffset"
        />

        <BrushTool
          v-model="activeTool"
          :bounds="bounds"
          @export="update"
        />
      </div>

      <canvas
        ref="canvas"
        resize
      />
    </div>
  </v-img>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'
import paper from 'paper'
import BrushTool from './tools/BrushTool.vue'
import SelectTool from './tools/SelectTool.vue'

const props = defineProps({
  tool: {
    type: String,
    default: 'select'
  },
  avatarText: {
    type: String,
    default: null
  }
})

const activeTool = ref()
watch(() => props.tool, (value) => {
  activeTool.value = value
}, { immediate: true })

const scope = new paper.PaperScope()
function setOffset(offset, subtract = true) {
  if (subtract) {
    offset = scope.view.center.subtract(offset)
  } else {
    offset = scope.view.center.add(offset)
  }
  scope.view.center = offset
}

const zoom = ref(0.2)
function changeZoom(delta, position) {
  const { center, zoom: oldZoom } = scope.view
  const factor = 1 + zoom.value
  const newZoom = delta < 0 ? oldZoom * factor : oldZoom / factor
  const beta = oldZoom / newZoom
  const x = position.subtract(center).multiply(beta)
  const offset = position.subtract(x).subtract(center)
  return { newZoom, offset }
}
function onWheel({ offsetX, offsetY, deltaY }) {
  const position = scope.view.viewToProject(
    new paper.Point(offsetX, offsetY),
  )
  const { newZoom, offset } = changeZoom(deltaY, position)
  if (newZoom < 10 && newZoom > 0.5) {
    scope.view.zoom = newZoom
    setOffset(offset, false)
  }
}

const emit = defineEmits(['load', 'error', 'update'])
const bounds = ref({
  xMin: 0,
  xMax: 0,
  yMin: 0,
  yMax: 0,
  width: 0,
  height: 0
})
function onLoad(src) {
  const raster = new paper.Raster(src)
  nextTick(() => {
    const { width, height } = raster.bounds
    const scale = Math.min(
      scope.view.bounds.width / width,
      scope.view.bounds.height / height
    )
    raster.scale(scale, scale)
    raster.position = scope.view.center
    bounds.value = {
      xMin: raster.bounds.x,
      xMax: raster.bounds.x + width * scale,
      yMin: raster.bounds.y,
      yMax: raster.bounds.y + height * scale,
      width: width * scale,
      height: height * scale
    }
    emit('load')
  })
}
function onError() {
  emit('error')
}
function update(values) {
  emit('update', values)
}

const canvas = ref()
onMounted(() => {
  const { offsetWidth, offsetHeight } = canvas.value.parentNode
  canvas.value.style.width = `${offsetWidth}px`
  canvas.value.style.height = `${offsetHeight}px`
  nextTick(() => {
    scope.setup(canvas.value)
    scope.activate()
  })
})
</script>

<style>
.v-img.image-wrapper {
  border-radius: 28px 0 0 28px;
}

.v-img.image-wrapper .v-img__img {
  display: none;
}
</style>

<style scoped>
canvas {
  width: 600px;
  height: 400px;
}

.canvas-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
