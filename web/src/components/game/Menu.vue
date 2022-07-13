<template>
  <v-menu
    v-model="menu"
    min-width="225"
    max-width="225"
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
      <v-list-item @click="goTo('game')">
        <v-list-item-content>
          {{ $t('game.fields.new-game') }}
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
    goTo(name) {
      if (this.isGame) {
        this.$store.commit('game/updateDialog', true);
      } else {
        this.$router.push({ name });
      }
      this.menu = false;
    },
  },
  computed: {
    isGame() {
      return this.$route.name === 'game';
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
