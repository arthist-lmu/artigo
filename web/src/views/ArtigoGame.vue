<template>
  <div id="artigo-game">
    <v-progress-linear :value="progress"></v-progress-linear>
    <h2>Only {{ secondsLeft }} seconds left!</h2>
    <v-img
      id="main-image"
      contain
      max-height="65vh"
      src="http://localhost:8000/media/36/21/36216392e7f137c39c006c698f8f2546.jpg"
    ></v-img>
    <v-container>
      <v-row>
        <v-text-field
          v-model="tagging"
          label="Discribe what you see"
          clearable
        ></v-text-field>
        <v-btn color="primary" depressed rounded> Enter </v-btn>
        <v-btn @click="get_res" color="accent" depressed rounded> Skip </v-btn>
      </v-row>
    </v-container>
  </div>
</template>

<style>
#main-image {
  margin: 5%;
}
</style>

<script>
export default {
  data() {
    return {
      tagging: "",
      secondsLeft: 30,
      timeLimit: 30,
      progress: 0,
    };
  },

  methods: {
    get_res() {
      this.$store.dispatch("resource/get", { random: true });
      this.dialog = false;
    },
  },

  watch: {
    secondsLeft: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.secondsLeft -= 1;
            this.progress = 100 - (100 / this.timeLimit) * this.secondsLeft;
            if (this.secondsLeft === 0) {
              this.get_res();
            }
          }, 1000);
        }
      },
      immediate: true, // This ensures the watcher is triggered upon creation
    },
  },
};
</script>
