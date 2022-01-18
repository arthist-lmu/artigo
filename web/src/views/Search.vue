<template>
  <PageTabs :items="items">
    <SearchCard />
  </PageTabs>
</template>

<script>
import PageTabs from '@/components/PageTabs.vue';
import SearchCard from '@/components/SearchCard.vue';

export default {
  computed: {
    items() {
      return [
        {
          title: this.$t('search.title'),
          texts: this.$t('search.texts'),
        },
      ];
    },
  },
  components: {
    PageTabs,
    SearchCard,
  },
};
</script>
