<template>
  <v-progress-linear
    :value="progress"
    :color="progress >= 85 ? 'error' : 'primary'"
  />
</template>

<script>
export default {
  props: {
    params: Object,
  },
  data() {
    return {
      timer: null,
      seconds: 0,
    };
  },
  computed: {
    progress() {
      return (this.seconds / this.duration) * 100;
    },
    duration() {
      return this.params.game_round_duration;
    },
  },
  destroyed() {
    clearInterval(this.timer);
  },
  created() {
    this.$emit('progress', this.seconds);
    this.timer = setInterval(() => {
      if (this.seconds === this.duration) {
        this.$emit('next');
      } else {
        this.seconds += 1;
        this.$emit('progress', this.seconds);
      }
    }, 1000);
  },
};
</script>

<style scoped>
.v-progress-linear {
  position: absolute;
  z-index: 99;
}
</style>
