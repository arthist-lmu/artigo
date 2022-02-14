<template>
  <v-card flat>
    <v-card-text>
      <div v-if="secondsLeft >= 0">
        <v-progress-linear :value="progress" />
      </div>

      <ImageCanvas
        :src="entry.path"
        selectType="rectangle"
        v-on:load="loaded"
        @mouseUp="update"
        class="my-4 grey lighten-2"
        height="70vh"
        contain
      />

      <v-container>
        <v-row>
          <v-col cols="8">
            <v-text-field
              v-model="tagging"
              ref="tagging"
              placeholder="Describe what you see"
              hide-details
              single-line
              clearable
            />
          </v-col>

          <v-col cols="4">
            <v-btn
              @click="postTag"
              class="mr-2"
              color="primary"
              width="calc(50% - 4px)"
              depressed
              rounded
            >
              Enter
            </v-btn>

            <v-btn
              @click="reload"
              color="accent"
              width="calc(50% - 4px)"
              depressed
              rounded
            >
              Skip
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      tagging: null,
      timeLimit: 30,
      secondsLeft: this.timeLimit,
    };
  },
  methods: {
    reload() {
      const random = this.getHash(new Date());
      const params = { random, limit: 1, sourceView: true };
      this.$store.dispatch('search/post', params).then(() => {
        clearInterval(this.timer);
        this.$refs.tagging.focus();
      });
    },
    loaded() {
      this.secondsLeft = this.timeLimit;
      this.timer = setInterval(() => {
        this.secondsLeft -= 1;
        if (this.secondsLeft === 0) {
          this.reload();
        }
      }, 1000);
    },
    update(values) {
      console.log(values);
    },
    postTag() {
      this.$store.dispatch('resource/post', {
        imgID: this.entry.path,
        tag: 'beautiful',
      });
    },
  },
  computed: {
    entry() {
      const { entries } = this.$store.state.search.data;
      return entries[0] || {};
    },
    progress() {
      return 100 - (100 / this.timeLimit) * this.secondsLeft;
    },
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  mounted() {
    this.$refs.tagging.focus();
  },
  created() {
    this.reload();
  },
  components: {
    ImageCanvas: () => import('@/components/ImageCanvas.vue'),
  },
};
</script>

<style scoped>
.v-input {
  padding-top: 0;
  margin-top: 0;
}
</style>
