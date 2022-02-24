<template>
  <v-snackbar
    v-model="display"
    :timeout="timeout"
    :color="color"
  >
    <span
      v-for="detail in details"
      :key="detail"
    >
      {{ keyInObj(detail, $t("error")) ? $t("error")[detail] : $t("error.unknown_error") }}
    </span>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      display: false,
      timeout: 5000,
    };
  },
  computed: {
    details() {
      return this.$store.state.utils.message.details;
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
