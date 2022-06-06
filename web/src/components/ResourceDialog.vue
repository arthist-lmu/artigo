<template>
  <v-dialog
    v-model="showModal"
    :retain-focus="false"
    max-width="750"
  >
    <ResourceCard :entry="entry"/>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      entry: null,
      showModal: false,
    };
  },
  computed: {
    data() {
      return this.$store.state.resource.data;
    },
  },
  watch: {
    data(value) {
      this.$store.commit('resource/updateData', null);
      if (value) {
        this.entry = value;
        this.showModal = true;
      }
    },
    $route() {
      this.showModal = false;
    },
  },
  components: {
    ResourceCard: () => import('@/components/ResourceCard.vue'),
  },
};
</script>
