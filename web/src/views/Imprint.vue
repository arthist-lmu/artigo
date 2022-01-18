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
          title: this.$t('imprint.title'),
          texts: this.$t('imprint.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs,
  },
};
</script>
