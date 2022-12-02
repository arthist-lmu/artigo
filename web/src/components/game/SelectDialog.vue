<template>
  <v-dialog
    v-model="dialog"
    :retain-focus="false"
    max-width="625"
    scrollable
    persistent
  >
    <SelectCard
      v-model="dialog"
      :defaultParams="params"
    />
  </v-dialog>
</template>

<script>
export default {
  props: {
    value: Boolean,
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    params() {
      return this.$store.state.game.dialog.params;
    },
  },
  watch: {
    dialog(value) {
      if (!value) {
        this.$store.commit('game/updateDialog', { params: {} });
      }
      this.$emit('input', value);
    },
    value: {
      handler(value) {
        this.dialog = value;
      },
      immediate: true,
    },
  },
  components: {
    SelectCard: () => import('./SelectCard.vue'),
  },
};
</script>
