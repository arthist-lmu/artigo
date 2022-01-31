<template>
  <PageTabs :items="items" />
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('privacy-policy.title'),
          texts: this.$t('privacy-policy.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
  },
};
</script>
