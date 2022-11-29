<template>
  <Layout opaque>
    <v-container
      v-if="!dialog"
      :class="[$vuetify.breakpoint.mdAndDown ? 'mobile px-1' : undefined, 'mt-8']"
      style="position: relative; height: calc(100% - 22px);"
    >
      <v-fade-transition>
        <Countdown
          v-if="countdown"
          :duration="3"
          @finish="onFinish"
        />
        <v-card
          v-else
          style="overflow: clip;"
          flat
        >
          <Progress
            v-if="!loading"
            :params="params"
            @next="next"
            @progress="progress"
          />

          <v-row>
            <v-col
              class="py-0"
              :cols="$vuetify.breakpoint.mdAndDown ? 12 : 8"
            >
              <ROICanvas
                v-if="gameType === 'roi'"
                tool="brush"
                :entry="entry"
                :params="params"
                @load="onLoad"
                @error="next"
              />
              <DefaultCanvas
                v-else
                :entry="entry"
                :params="params"
                @load="onLoad"
                @error="next"
              />
            </v-col>

            <v-col
              v-if="!loading"
              class="py-0"
              :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4"
            >
              <TaggingSidebar
                v-if="gameType === 'tagging'"
                :entry="entry"
                :params="params"
                :seconds="seconds"
                @next="next"
              />
              <DefaultSidebar
                v-else
                :entry="entry"
                :params="params"
                :seconds="seconds"
                @next="next"
              />
            </v-col>
          </v-row>
        </v-card>
      </v-fade-transition>
    </v-container>
  </Layout>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      path: null,
      seconds: 0,
      loading: true,
      countdown: false,
    };
  },
  methods: {
    get() {
      this.$store.commit('game/updateDialog', { show: true });
    },
    next() {
      if (this.roundId === this.rounds) {
        const { sessionId: id } = this.$store.state.game;
        this.$router.push({ name: 'session', params: { id } });
      } else {
        this.countdown = true;
        this.loading = true;
      }
    },
    onLoad() {
      this.path = this.entry.path;
    },
    onFinish() {
      this.$store.dispatch('game/get', {}).then(() => {
        this.countdown = false;
      });
    },
    progress(seconds) {
      this.seconds = seconds;
    },
  },
  computed: {
    ...mapState('game', [
      'entry',
      'params',
      'roundId',
      'rounds',
    ]),
    dialog() {
      return this.$store.state.game.dialog.show;
    },
    gameType() {
      return this.params.game_type;
    },
  },
  watch: {
    '$route.params.lang'() {
      this.get();
    },
    path() {
      this.$nextTick(() => {
        this.loading = false;
      });
    },
  },
  beforeRouteUpdate() {
    this.get();
  },
  mounted() {
    this.$store.dispatch('game/getURLParams', this.$route.query);
    window.onpopstate = () => {
      this.$store.dispatch('game/getURLParams', this.$route.query);
    };
    this.$nextTick(() => {
      this.get();
    });
  },
  components: {
    Layout: () => import('@/layouts/Default.vue'),
    Progress: () => import('@/components/game/Progress.vue'),
    Countdown: () => import('@/components/Countdown.vue'),
    DefaultCanvas: () => import('@/components/game/canvas/Default.vue'),
    ROICanvas: () => import('@/components/game/canvas/ROI.vue'),
    DefaultSidebar: () => import('@/components/game/sidebar/Default.vue'),
    TaggingSidebar: () => import('@/components/game/sidebar/Tagging.vue'),
  },
};
</script>

<style scoped>
.container div:not([role=progressbar]) {
  height: 100%;
}

.container.mobile .row {
  height: 50%;
}
</style>
