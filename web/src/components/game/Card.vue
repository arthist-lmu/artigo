<template>
  <v-hover v-slot="{ hover }">
    <div
      @click="play"
      @keydown="play"
      class="grid-item"
      :disabled="isDisabled"
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
              v-if="tabooType"
              :title="$t(`home.plugins.taboos.${'most_annotated_taboo'}`)"
              class="ml-2"
              x-small
              fab
            >
              <v-icon color="primary">
                mdi-tag-off-outline
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>

        <v-row></v-row>

        <v-row style="flex: 0;">
          <v-col class="pa-4">
            <div class="text-subtitle-1 white--text">
              <p v-html="$t(`home.fields.${entry.type}`, { value: `<b>${entry.query}</b>` })"></p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
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
      const params = { show: false, params: this.entry.params };
      this.$store.commit('game/updateDialog', params);
      this.$router.push({ name: 'game' });
    },
    onError() {
      this.isDisabled = true;
    },
  },
  computed: {
    gameType() {
      return this.entry.params.game_type;
    },
    tabooType() {
      return this.entry.params.taboo_type;
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
