<template>
  <v-snackbar
    v-model="display"
    class="mb-10"
    :timeout="timeout"
    color="primary"
    rounded
    dark
  >
    <span>{{ $t('search.fields.game') }}</span>

    <v-btn
      @click="goToGame()"
      class="ml-4 mr-n2"
      depressed
      rounded
      small
    >
      {{ $t('field.off-we-go') }}

      <v-icon
        class="ml-1 mr-n1"
        small
      >
        mdi-play
      </v-icon>
    </v-btn>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      display: false,
      timeout: -1,
    };
  },
  methods: {
    goToGame() {
      const entries = this.entries.map(({ resource_id }) => resource_id);
      const params = {
        resource_inputs: entries,
        resource_type: 'custom_resource',
      };
      this.$store.commit('game/updateDialog', { params });
      this.$router.push({ name: 'game' });
    },
  },
  computed: {
    entries() {
      return this.$store.state.search.data.entries;
    },
  },
  watch: {
    entries(values) {
      if (values && values.length) {
        this.display = true;
      }
    },
  },
};
</script>

<style scoped>
.v-snack {
  z-index: 200 !important;
}
</style>
