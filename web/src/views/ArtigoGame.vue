<template>
  <div>
    <v-progress-linear
        :value="progress"
    ></v-progress-linear>
    <h2> Only {{ secondsLeft }} seconds left! </h2>
    <v-img
    src="http://localhost:8000/media/36/21/36216392e7f137c39c006c698f8f2546.jpg"
    ></v-img>
    <v-container>
    <v-row>
      <v-text-field
        v-model="tagging"
        solo
        label="Discribe what you see"
        clearable
      ></v-text-field>
      <v-btn
        color="primary"
        heigth="50"
      >
      Primary
      </v-btn>
      <v-btn
          @click="get_res"
          color="accent"
          depressed
          rounded
          block
        >
          {{ data }} 
        </v-btn>
    </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tagging: "",
      secondsLeft: 40,
      timeLimit: 40,
      progress: 0,
    };
  },

  methods: {
    get_res() {
      this.$store.dispatch('resource/get', { random: true });
      this.dialog = false;
    },
  },

  watch: {
    secondsLeft: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.secondsLeft -= 1;
            this.progress = 100 - ((100 / this.timeLimit) * this.secondsLeft);
          }, 1000);
        }
      },
      immediate: true, // This ensures the watcher is triggered upon creation
    },
  },
};
</script>
