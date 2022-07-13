<template>
  <v-dialog
    v-model="dialog"
    :retain-focus="false"
    :persistent="isGame"
    max-width="625"
  >
    <SelectCard
      v-model="dialog"
      :persistent="isGame"
    />
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    show() {
      return this.$store.state.game.dialog;
    },
    isGame() {
      return this.$route.name === 'game';
    },
  },
  watch: {
    dialog(value) {
      if (!value) {
        this.$store.commit('game/updateDialog', false);
      }
    },
    show: {
      handler(value) {
        if (value) {
          this.dialog = true;
        }
      },
      immediate: true,
    },
    $route() {
      this.dialog = false;
    },
  },
  components: {
    SelectCard: () => import('./SelectCard.vue'),
  },
};
</script>
