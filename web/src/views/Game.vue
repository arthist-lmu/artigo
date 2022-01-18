<template>
  <div>
    <v-progress-linear :value="progress" />
    <h2>{{ secondsLeft }} seconds</h2>

    <v-img
      :src="data.path"
      id="main-image"
      height="70vh"
      contain
    />

    <v-container>
      <v-row>
        <v-text-field
          v-model="tagging"
          label="Describe what you see"
          clearable
          ref="taggingBox"
        />

        <v-btn
          @click="postTag"
          class="mr-2"
          color="primary"
          depressed
          rounded
        >
          Enter
        </v-btn>

        <v-btn
          @click="getRes"
          color="accent"
          depressed
          rounded
        >
          Skip
        </v-btn>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tagging: null,
      timeLimit: 30,
      secondsLeft: this.timeLimit,
    };
  },
  methods: {
    getRes() {
      console.log('Download new image');
      this.$store.dispatch('resource/get', { random: true }).then(() => {
        this.secondsLeft = this.timeLimit;
      });
    },
    postTag() {
      this.$store.dispatch('resource/post', {
        imgID: this.data.path,
        tag: 'beautiful',
      });
    },
    displayImgUrl() {
      console.log(this.data.path);
    },
  },
  computed: {
    data() {
      return this.$store.state.resource.data;
    },
    progress() {
      return 100 - (100 / this.timeLimit) * this.secondsLeft;
    },
    tags() {
      if (this.keyInObj('tags', this.data)) {
        if (this.moreTags && this.data.tags.length > 20) {
          return this.data.tags.slice(0, 20);
        }
        return this.data.tags;
      }
      return [];
    },
  },
  watch: {
    secondsLeft: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.secondsLeft -= 1;
            if (this.secondsLeft === 0) {
              this.getRes();
            }
          }, 1000);
        }
      },
      immediate: true,
    },
    '$route.params.id'(id) {
      this.getData(id);
    },
  },
  mounted() {
    this.$refs.taggingBox.focus();
  },
  created() {
    this.getRes();
  },
};
</script>

<style scoped>
</style>
