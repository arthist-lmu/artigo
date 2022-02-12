<template>
  <v-snackbar
    v-model="display"
    :timeout="timeout"
    :color="color"
  >
    {{ keyInObj(detail, $t("error")) ? $t("error")[detail] : $t("error.unknown_error") }}
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      display: false,
      timeout: 2500,
    };
  },
  computed: {
    detail() {
      return this.$store.state.utils.message.detail;
    },
    timestamp() {
      return this.$store.state.utils.message.timestamp;
    },
    color() {
      const { type } = this.$store.state.utils.message;
      if (type === 'error') {
        return 'error';
      }
      return 'primary';
    },
  },
  watch: {
    timestamp() {
      this.display = true;
    },
  },
};
</script>
