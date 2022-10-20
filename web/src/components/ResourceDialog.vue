<template>
  <v-dialog
    v-model="dialog"
    :retain-focus="false"
    max-width="750"
    scrollable
  >
    <ResourceCard
      key="entry.id"
      :entry="entry"
    />
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      entry: null,
      dialog: false,
    };
  },
  computed: {
    show() {
      return this.$store.state.resource.data;
    },
  },
  watch: {
    dialog(value) {
      if (!value) {
        this.$store.commit('resource/updateData', null);
      }
    },
    show(value) {
      if (value) {
        this.entry = value;
        this.dialog = true;
      }
    },
    $route() {
      this.dialog = false;
    },
  },
  components: {
    ResourceCard: () => import('@/components/ResourceCard.vue'),
  },
};
</script>
