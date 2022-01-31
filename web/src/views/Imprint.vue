<template>
  <PageTabs :items="items" />
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('imprint.title'),
          texts: this.$t('imprint.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
  },
};
</script>
