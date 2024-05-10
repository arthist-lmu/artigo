import { computed } from 'vue'
import paper from 'paper'

export default function useTool(name, modelValue) {
  const tool = new paper.Tool({
    minDistance: 10,
    maxDistance: 45
  })

  function getRoi({
    x, y, width, height
  }, bounds, relative = true) {
    if (width == null) {
      width = 0
    }
    if (height == null) {
      height = 0
    }
    if (relative) {
      const {
        xMin, width: imgWidth,
        yMin, height: imgHeight
      } = bounds
      x = (x - xMin) / imgWidth
      y = (y - yMin) / imgHeight
      width /= imgWidth
      height /= imgHeight
    }
    return {
      x, y, width, height,
    }
  }

  const isActive = computed(() => modelValue === name)
  const isDisabled = computed(() => false)

  return {
    tool,
    getRoi,
    isActive,
    isDisabled
  }
}
