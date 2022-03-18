<template>
  <v-container>
    {{ entries }}
  </v-container>
</template>

<script>
export default {
  methods: {
    get(id) {
      this.$store.dispatch('session/get', { id });
    },
  },
  computed: {
    entries() {
      return this.$store.state.session.data;
    },
  },
  watch: {
    '$route.params.id'(id) {
      this.get(id);
    },
  },
  created() {
    this.get(this.$route.params.id);
  },
};
</script>
