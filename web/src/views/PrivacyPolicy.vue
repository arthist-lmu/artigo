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
          title: this.$t('privacy-policy.title'),
          texts: this.$t('privacy-policy.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs,
  },
};
</script>
