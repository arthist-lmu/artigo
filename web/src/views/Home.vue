<template>
  <v-card flat>
    <v-card-text>
      <v-img
        :src="entry.path"
        @click="showDialog"
        class="grey lighten-2"
        max-height="70vh"
        style="cursor: pointer;"
        contain
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    showDialog() {
      this.$store.commit('resource/updateData', this.entry);
    },
  },
  computed: {
    entry() {
      const { entries } = this.$store.state.search.data;
      return entries[0] || {};
    },
    maxHeight() {
      let height = this.getHeight('main', false);
      const { clientHeight } = document.documentElement;
      height = (clientHeight - height) + 32;
      return `calc(100vh - ${height}px)`;
    },
  },
  created() {
    const random = (new Date()).setHours(0, 0, 0, 0);
    const params = { random, limit: 1, sourceView: true };
    this.$store.dispatch('search/post', params);
  },
};
</script>
