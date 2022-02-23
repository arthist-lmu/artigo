<template>
  <v-card flat>
    <v-card-text>
      <v-dialog
        v-model="showModal"
        max-width="750"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-img
            :src="entry.path"
            class="grey lighten-2"
            max-height="70vh"
            v-bind="attrs"
            v-on="on"
            style="cursor: pointer;"
            contain
          />
        </template>

        <ResourceCard
          :entry="entry"
          :showImage="false"
        />
      </v-dialog>
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
    const today = (new Date()).setHours(0, 0, 0, 0);
    const random = this.getHash(today);
    const params = { random, limit: 1, sourceView: true };
    this.$store.dispatch('search/post', params);
  },
  components: {
    ResourceCard: () => import('@/components/ResourceCard.vue'),
  },
};
</script>
