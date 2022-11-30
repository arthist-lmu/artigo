<template>
  <v-btn
    @click="goToGame()"
    :title="$t('game.title')"
    :dark="dark"
    class="play"
    depressed
    x-small
  >
    <v-icon :color="dark ? 'accent' : 'primary'">
      mdi-play
    </v-icon>
  </v-btn>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    goToGame() {
      const values = { show: false, params: {} };
      switch (this.$route.name) {
        case 'game': {
          values.show = true; // force dialog to open
          break;
        }
        case 'search': {
          let { entries } = this.$store.state.search.data;
          entries = entries.map(({ resource_id }) => resource_id);
          values.params.resource_inputs = entries;
          values.params.resource_type = 'custom_resource';
          break;
        }
        default:
          break;
      }
      this.$store.commit('game/updateDialog', values);
      this.$router.push({ name: 'game' });
    },
  },
};
</script>

<style scoped>
.play {
  margin-left: -52px;
  width: 44px;
}

.play, .play::before {
  border-radius: 12px;
}
</style>
