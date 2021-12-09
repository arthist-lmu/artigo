<template>
  <div>
    <v-progress-linear
        :value="progress"
    ></v-progress-linear>
    <h2> Only {{ secondsLeft }} seconds left! </h2>
  </div>
</template>

<script>
export default {
  data() {
    return {
      secondsLeft: 40,
      timeLimit: 40,
      progress: 0,
    };
  },

  watch: {
    secondsLeft: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.secondsLeft -= 1;
            this.progress = 100 - ((100 / this.timeLimit) * this.secondsLeft);
            console.log(this.progress)
          }, 1000);
        }
      },
      immediate: true, // This ensures the watcher is triggered upon creation
    },
  },
};
</script>
