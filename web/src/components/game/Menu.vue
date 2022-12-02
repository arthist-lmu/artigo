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
      const params = {};
      if (this.$route.name === 'search') {
        let { entries } = this.$store.state.search.data;
        entries = entries.map(({ resource_id }) => resource_id);
        params.resource_inputs = entries;
        params.resource_type = 'custom_resource';
      }
      this.$store.commit('/game/updateDialog', { params });
      if (this.$route.name === 'game') {
        const path = `/${this.$i18n.locale}/game`;
        this.$router.push({ path: `${path}?id=${Date.now()}` });
      } else {
        this.$router.push({ name: 'game' });
      }
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
