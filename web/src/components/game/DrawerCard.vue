<template>
  <v-hover
    v-if="!isDisabled"
    v-slot="{ hover }"
  >
    <v-card
      v-if="entry.path"
      @click="play"
      @keydown="play"
      class="grid-item"
      :disabled="isDisabled"
      flat
    >
      <img
        :src="entry.path"
        v-on:error="onError"
        alt=""
      />

      <v-fade-transition>
        <v-container v-if="hover">
          <v-row
            justify="center"
            align="center"
          >
            <v-col cols="auto">
              <v-btn
                color="primary"
                large
                fab
              >
                <v-icon color="accent">
                  mdi-play
                </v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-fade-transition>

      <v-container class="overlay">
        <v-row style="flex: 0;">
          <v-col
            class="pa-4"
            align="right"
          >
            <v-btn
              v-if="gameType === 'roi'"
              :title="$t('home.game_type.roi')"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-draw
              </v-icon>
            </v-btn>
            <v-btn
              v-else
              :title="$t('home.game_type.tagging')"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-tag-outline
              </v-icon>
            </v-btn>

            <v-btn
              v-if="opponentType === 'no_opponent'"
              :title="$t(`home.plugins.opponent_type.${opponentType}`)"
              class="ml-2"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-account-off-outline
              </v-icon>
            </v-btn>

            <v-btn
              v-if="tabooType && !tabooType.startsWith('no_')"
              :title="$t(`home.plugins.taboo_type.${tabooType}`)"
              class="ml-2"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-filter-outline
              </v-icon>
            </v-btn>

            <v-btn
              v-if="suggesterType && !suggesterType.startsWith('no_')"
              :title="$t(`home.plugins.suggester_type.${suggesterType}`)"
              class="ml-2"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-lightbulb-variant-outline
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>

        <v-row></v-row>

        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <p v-if="title && title[lang]">
                {{ title[lang] }}
              </p>
              <p
                v-else
                v-html="$t(`home.fields.${entry.type}`, { value: entry.query })"
              />
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <v-btn
      v-else
      @click="play"
      @keydown="play"
      color="grey lighten-2"
      depressed
      outlined
      rounded
      block
    >
      <template v-if="title && title[lang]">
        {{ title[lang] }}
      </template>
      <template v-else>
        {{ $t("game.fields.new-game-default") }}
      </template>
    </v-btn>
  </v-hover>
</template>

<script>
export default {
  props: {
    entry: Object,
  },
  data() {
    return {
      isDisabled: false,
    };
  },
  methods: {
    play() {
      if (this.entry.params) {
        this.$store.commit('game/updateDialog', { params: this.entry.params });
      }
      this.$router.push({ name: 'game' });
    },
    onError() {
      this.isDisabled = true;
    },
  },
  computed: {
    lang() {
      return this.$i18n.locale;
    },
    title() {
      return this.entry.title;
    },
    gameType() {
      return this.entry.params.game_type;
    },
    opponentType() {
      return this.entry.params.opponent_type;
    },
    tabooType() {
      return this.entry.params.taboo_type;
    },
    suggesterType() {
      return this.entry.params.suggester_type;
    },
  },
};
</script>

<style scoped>
.grid-item {
  border-radius: 28px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  display: block;
  height: 225px;
  flex-grow: 1;
}

.grid-item[disabled] {
  display: none;
}

.grid-item > img {
  transition: transform 0.5s ease;
  transform: scale(1.05);
  object-position: top;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  height: 100%;
}

.grid-item:hover > img {
  transform: scale(1.3);
}

.container {
  flex-direction: column;
  position: absolute;
  display: flex;
  height: 100%;
  z-index: 99;
  width: 100%;
  bottom: 0;
  left: 0;
}

.container p {
  line-height: 1.25rem;
  margin-bottom: 0;
}

.container p::first-letter {
  text-transform: uppercase;
}

.container .overlay {
  background: linear-gradient(to top, black, #00000000 40%);
  transform: translate(-50%, -50%);
  position: absolute;
  object-fit: cover;
  min-width: 100%;
  max-width: 100%;
  color: #ffffff;
  height: 100%;
  left: 50%;
  top: 50%;
}
</style>
