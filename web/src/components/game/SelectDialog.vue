<template>
  <v-dialog
    v-model="dialog"
    :retain-focus="false"
    :persistent="isGame"
    max-width="625"
    scrollable
  >
    <SelectCard
      v-model="dialog"
      :persistent="isGame"
      :defaultParams="params"
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
      return this.$store.state.game.dialog.show;
    },
    params() {
      return this.$store.state.game.dialog.params;
    },
    isGame() {
      return this.$route.name === 'game';
    },
  },
  watch: {
    dialog(value) {
      if (!value) {
        const values = { show: false, params: {} };
        this.$store.commit('game/updateDialog', values);
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
  mounted() {
    window.onpopstate = () => {
      this.dialog = false;
    };
  },
  components: {
    SelectCard: () => import('./SelectCard.vue'),
  },
};
</script>
