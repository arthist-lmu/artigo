<template>
  <v-snackbar
    v-model="display"
    :timeout="timeout"
    :color="color"
  >
    {{ detail }}
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      display: false,
      timeout: 2000,
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
