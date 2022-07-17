<template>
  <span ref="container">
    <slot name="prepend-item"></slot>
    <span class="typing"></span>
  </span>
</template>

<script>
import Typed from 'typed.js';

export default {
  props: {
    strings: {
      type: Array,
      required: true,
    },
    typeSpeed: {
      type: Number,
      required: false,
      default: 75,
    },
    startDelay: {
      type: Number,
      required: false,
      default: 100,
    },
    backSpeed: {
      type: Number,
      required: false,
      default: 50,
    },
    smartBackspace: {
      type: Boolean,
      required: false,
      default: true,
    },
    removeBackspace: {
      type: Boolean,
      required: false,
      default: true,
    },
    backDelay: {
      type: Number,
      required: false,
      default: 2000,
    },
    loop: {
      type: Boolean,
      required: false,
      default: true,
    },
    loopCount: {
      type: Number,
      required: false,
      default: Infinity,
    },
  },
  data() {
    return {
      typer: null,
    };
  },
  methods: {
    handlers(config) {
      config.onStop = () => {
        this.$emit('onStop');
      };

      config.onStart = () => {
        this.$emit('onStart');
      };

      config.onReset = () => {
        this.$emit('onReset');
      };

      config.onDestroy = () => {
        this.$emit('onDestroy');
      };

      config.onComplete = () => {
        if (!this.loop && this.removeBackspace) {
          this.$refs.container.querySelector('.typed-cursor').remove();
        }
        this.$emit('onComplete');
      };

      return config;
    },
    init() {
      const element = this.$refs.container.querySelector('.typing');
      const config = this.handlers(this.$props);
      this.typer = new Typed(element, config);
    },
  },
  destroyed() {
    this.typer.destroy();
  },
  mounted() {
    this.init();
  },
};
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
