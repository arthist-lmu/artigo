<template>
  <v-menu
    v-model="menu"
    min-width="225"
    max-width="325"
    :close-on-content-click="false"
    offset-y
    bottom
  >
    <template v-slot:activator="{ attrs, on }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        :title="$t('game.title')"
        class="play"
        depressed
        x-small
      >
        <v-icon :color="dark ? 'accent' : 'primary'">
          mdi-play
        </v-icon>
      </v-btn>
    </template>

    <v-list dense>
      <v-list-item @click="goToGame()">
        <v-list-item-content>
          {{ $t('game.fields.new-game-default') }}
        </v-list-item-content>
      </v-list-item>

      <v-list-item
        v-if="isSearch"
        @click="goToGame()"
      >
        <v-list-item-content>
          {{ $t('game.fields.new-game-search') }}
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      menu: false,
    };
  },
  methods: {
    goToGame() {
      const values = { show: false, params: {} };
      if (this.isSearch) {
        let { entries } = this.$store.state.search.data;
        entries = entries.map(({ resource_id }) => resource_id);
        values.params.resource_inputs = entries;
        values.params.resource_type = 'custom_resource';
      } else if (this.isGame) {
        values.show = true; // force dialog to open
      }
      this.$store.commit('game/updateDialog', values);
      this.$router.push({ name: 'game' });
      this.menu = false;
    },
  },
  computed: {
    isGame() {
      return this.$route.name === 'game';
    },
    isSearch() {
      return this.$route.name === 'search';
    },
  },
};
</script>

<style scoped>
.play {
  margin-left: -58px;
  width: 48px;
}

.play::before {
  border-radius: 12px;
}
</style>
