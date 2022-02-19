<template>
  <v-btn
    @click="reconcile"
    :title="$t('reconcile.title')"
    class="ml-1 mr-n2"
    color="primary"
    icon
  >
    <v-icon>mdi-wiper</v-icon>
  </v-btn>
</template>

<script>
export default {
  props: {
    entryId: String,
    name: String,
    type: String,
  },
  methods: {
    reconcile() {
      const queries = [{ name: this.name, type: this.type }];
      this.$store.dispatch('reconcile/post', { queries });
    },
  },
};
</script>
