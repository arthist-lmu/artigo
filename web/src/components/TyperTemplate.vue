<template>
  <span ref="container">
    <slot name="prepend-item" />
    <span class="typing" />
  </span>
</template>

<script setup>
import Typed from 'typed.js'
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  strings: {
    type: Array,
    required: true
  },
  typeSpeed: {
    type: Number,
    required: false,
    default: 75
  },
  startDelay: {
    type: Number,
    required: false,
    default: 100
  },
  backSpeed: {
    type: Number,
    required: false,
    default: 50
  },
  smartBackspace: {
    type: Boolean,
    required: false,
    default: true
  },
  removeBackspace: {
    type: Boolean,
    required: false,
    default: true
  },
  backDelay: {
    type: Number,
    required: false,
    default: 2000
  },
  loop: {
    type: Boolean,
    required: false,
    default: true
  },
  loopCount: {
    type: Number,
    required: false,
    default: Infinity
  }
})

let typer = null
const container = ref()

function init() {
  const element = container.value.querySelector('.typing')
  typer = new Typed(element, handlers(props))
}
onMounted(() => init())
onUnmounted(() => typer.destroy())

const emit = defineEmits([
  'onStop',
  'onStart',
  'onReset',
  'onDestroy',
  'onComplete'
])
function handlers(config) {
  config.onStop = () => {
    emit('onStop')
  }

  config.onStart = () => {
    emit('onStart')
  }

  config.onReset = () => {
    emit('onReset')
  }

  config.onDestroy = () => {
    emit('onDestroy')
  }

  config.onComplete = () => {
    if (!config.loop && config.removeBackspace) {
      container.value.querySelector('.typed-cursor').remove()
    }
    emit('onComplete')
  }

  return config
}
</script>

<style>
.typed-cursor {
  animation: typing 2s infinite;
  color: #e26162;
  opacity: 1;
}

.typed-cursor.disabled {
  display: none;
}

@keyframes typing {
  50% { opacity: 0; }
}
</style>
