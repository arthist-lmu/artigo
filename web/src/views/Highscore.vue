<template>
  <PageTabs :items="items" />
</template>

<script>
import PageTabs from '@/components/PageTabs.vue';

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
    PageTabs,
  },
};
</script>
