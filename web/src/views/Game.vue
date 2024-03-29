<template>
  <v-container
    :class="[$vuetify.breakpoint.mdAndDown ? 'mobile px-1' : undefined, 'mt-8']"
    style="position: relative; height: calc(100% - 22px);"
  >
    <template v-if="!dialog.inital">
      <v-fade-transition>
        <Countdown
          v-if="countdown"
          :duration="3"
          @finish="finishGameround"
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
              :key="path"
              :cols="$vuetify.breakpoint.mdAndDown ? 12 : 4"
            >
              <TaggingSidebar
                v-if="gameType === 'tagging'"
                :entry="entry"
                :params="params"
                :seconds="seconds"
                @next="next"
                @finish="finishGamesession"
              />
              <DefaultSidebar
                v-else
                :entry="entry"
                :params="params"
                :seconds="seconds"
                @next="next"
                @finish="finishGamesession"
              />
            </v-col>
          </v-row>
        </v-card>
      </v-fade-transition>
    </template>

    <SelectDialog v-model="dialog.inital" />

    <v-dialog
      v-model="dialog.helper"
      max-width="400"
    >
      <HelperCard
        v-model="dialog.helper"
        :text="$t('game.helper')"
        icon="mdi-help-circle-outline"
        page="about"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      path: null,
      seconds: 0,
      dialog: {
        inital: false,
        helper: false,
      },
      loading: true,
      countdown: false,
    };
  },
  methods: {
    get() {
      this.dialog.inital = true;
    },
    next() {
      if (this.roundId === this.rounds) {
        this.finishGamesession();
      } else {
        this.countdown = true;
        this.loading = true;
      }
    },
    onLoad() {
      if (!this.$store.state.utils.status.loading) {
        this.path = this.entry.path;
      }
    },
    finishGameround() {
      this.$store.dispatch('game/get', {}).then(() => {
        this.countdown = false;
      });
    },
    finishGamesession() {
      const { sessionId: id } = this.$store.state.game;
      this.$router.push({ name: 'session', params: { id } });
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
    'dialog.inital'(value) {
      if (value) {
        if (localStorage.getItem('gameHelper') === null) {
          localStorage.setItem('gameHelper', true);
          setTimeout(() => {
            this.$nextTick(() => {
              this.dialog.helper = true;
            });
          }, 250);
        }
        this.loading = true;
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    this.loading = true;
    this.$nextTick(() => {
      next();
    });
  },
  beforeRouteUpdate() {
    this.get();
  },
  mounted() {
    this.$store.dispatch('game/getURLParams', this.$route.query);
    window.onpopstate = () => {
      this.$store.dispatch('game/getURLParams', this.$route.query);
      this.loading = true;
    };
    this.$nextTick(() => {
      this.get();
    });
  },
  components: {
    Progress: () => import('@/components/game/Progress.vue'),
    Countdown: () => import('@/components/Countdown.vue'),
    DefaultCanvas: () => import('@/components/game/canvas/Default.vue'),
    ROICanvas: () => import('@/components/game/canvas/ROI.vue'),
    DefaultSidebar: () => import('@/components/game/sidebar/Default.vue'),
    TaggingSidebar: () => import('@/components/game/sidebar/Tagging.vue'),
    SelectDialog: () => import('@/components/game/SelectDialog.vue'),
    HelperCard: () => import('@/components/HelperCard.vue'),
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
