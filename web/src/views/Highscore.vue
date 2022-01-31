<template>
  <PageTabs :items="items" />
</template>

<script>
export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('highscore.title'),
          texts: this.$t('highscore.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs: () => import('@/components/PageTabs.vue'),
  },
};
</script>
