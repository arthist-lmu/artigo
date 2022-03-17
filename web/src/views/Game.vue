<template>
  <v-card flat>
    <v-card-text>
      <div v-if="seconds >= 0">
        <v-progress-linear :value="progress" />
      </div>

      <ImageCanvas
        v-if="entry"
        :src="entry.path"
        @load="loaded"
        @error="onError"
        class="my-4 grey lighten-2"
        height="70vh"
        contain
      />

      <v-container>
        <v-row>
          <v-col cols="8">
            <v-text-field
              v-model="tag"
              ref="tag"
              @keyup.enter.native="post"
              :placeholder="$t('game.fields')[gameType].placeholder"
              tabindex="1"
              hide-details
              single-line
              clearable
            />
          </v-col>

          <v-col cols="4">
            <v-btn
              @click="post"
              class="mr-2"
              color="primary"
              width="calc(50% - 4px)"
              depressed
              rounded
            >
              {{ $t("game.fields.basic.enter") }}
            </v-btn>

            <v-btn
              @click="nextRound"
              color="accent"
              width="calc(50% - 4px)"
              depressed
              rounded
            >
              {{ $t("game.fields.basic.skip") }}
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
      tag: null,
      timer: null,
      seconds: 0,
      rounds: 5,
      roundDuration: 60,
    };
  },
  methods: {
    get() {
      const params = {
        rounds: this.rounds,
        round_duration: this.roundDuration,
        opponent_type: 'random_gameround_opponent',
        lt_percentile: 0.75,
        score_types: [
          'annotations_validated_score',
          'opponent_validated_score',
        ],
        language: this.$i18n.locale,
      };
      if (this.gameType === 'taboo') {
        params.taboo_type = 'most_annotated_taboo';
        params.taboo_max_tags = 7;
      } else if (this.gameType === 'tag-a-tag') {
        // TODO
      }
      this.$store.dispatch('game/get', params).then(() => {
        this.tag = null;
      });
    },
    post() {
      if (this.tag.length) {
        const params = {
          tag: this.tag,
          resource_id: this.entry.resource_id,
          language: this.$i18n.locale,
        };
        this.$store.dispatch('game/post', params).then(() => {
          this.tag = null;
          this.$refs.tag.focus();
        });
      }
    },
    loaded() {
      this.seconds = 0;
      clearInterval(this.timer);
      this.timer = setInterval(() => {
        if (this.seconds === this.roundDuration) {
          this.nextRound();
        } else {
          this.seconds += 1;
        }
      }, 1000);
    },
    onError() {
      this.nextRound();
    },
    nextRound() {
      this.$store.dispatch('game/get', {});
    },
  },
  computed: {
    entry() {
      return this.$store.state.game.entry;
    },
    progress() {
      return (this.seconds / this.roundDuration) * 100;
    },
    gameType() {
      return this.$route.query.type || 'default';
    },
    status() {
      const { error, loading } = this.$store.state.utils.status;
      return !loading && error;
    },
  },
  watch: {
    entry() {
      this.$refs.tag.focus();
    },
    status(value) {
      if (value) {
        clearInterval(this.timer);
      }
    },
    seconds(value) {
      this.$store.dispatch('game/setSeconds', value);
    },
    '$route.params.lang'() {
      this.get();
    },
    '$route.query.type'() {
      this.get();
    },
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  beforeRouteUpdate() {
    // TODO: this does not work
    this.get();
  },
  mounted() {
    this.$nextTick(() => {
      this.get();
    });
  },
  components: {
    ImageCanvas: () => import('@/components/annotator/ImageCanvas.vue'),
  },
};
</script>

<style scoped>
.v-input {
  padding-top: 0;
  margin-top: 0;
}
</style>
