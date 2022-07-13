<template>
  <v-snackbar
    v-model="display"
    class="mb-10"
    :timeout="timeout"
    :color="color"
    :dark="color === 'primary'"
    rounded
  >
    <span
      v-for="detail in details"
      :key="detail"
    >
      {{ keyInObj(detail, $t("messages")) ? $t(`messages.${detail}`) : $t("messages.unknown_error") }}
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
      return type === 'error' ? 'error' : 'primary';
    },
  },
  watch: {
    timestamp() {
      this.display = true;
    },
  },
};
</script>
