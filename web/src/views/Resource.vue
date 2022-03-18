<template>
  <v-container v-if="exists">
    <ResourceCard :entry="entry" />
  </v-container>
</template>

<script>
export default {
  methods: {
    get(id) {
      this.$store.dispatch('resource/get', { id });
    },
  },
  computed: {
    entry() {
      return this.$store.state.resource.data;
    },
    exists() {
      return this.entry && Object.keys(this.entry).length;
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
  components: {
    ResourceCard: () => import('@/components/ResourceCard.vue'),
  },
};
</script>
