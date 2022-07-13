<template>
  <div class="loading">
    <v-hover v-slot="{ hover }">
      <div>
        <v-btn
          v-if="paused"
          @click="togglePause"
          color="primary"
          x-large
          fab
        >
          <v-icon>
            mdi-play
          </v-icon>
        </v-btn>
        <template v-else>
          <v-btn
            v-if="hover"
            @click="togglePause"
            color="primary"
            x-large
            fab
          >
            <v-icon>
              mdi-pause
            </v-icon>
          </v-btn>
          <v-btn
            v-else
            :color="duration - seconds < 1 ? 'error' : 'primary'"
            x-large
            fab
          >
            {{ duration - seconds }}
          </v-btn>
        </template>
      </div>
    </v-hover>
  </div>
</template>

<script>
export default {
  props: {
    params: Object,
    duration: {
      type: Number,
      default: 3,
    },
  },
  data() {
    return {
      timer: null,
      seconds: 0,
      paused: false,
    };
  },
  methods: {
    togglePause() {
      this.paused = !this.paused;
    },
  },
  computed: {
    progress() {
      return (this.seconds / this.duration) * 100;
    },
  },
  destroyed() {
    clearInterval(this.timer);
  },
  created() {
    this.timer = setInterval(() => {
      if (!this.paused) {
        if (this.seconds === this.duration) {
          this.$emit('finish');
        } else {
          this.seconds += 1;
        }
      }
    }, 1000);
  },
};
</script>

<style scoped>
.loading {
  position: absolute;
  z-index: 99;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
