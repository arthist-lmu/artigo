<template>
  <v-container class="pt-0">
    <SearchBar store="collections" />

    <DataIterator
      :component="component"
      store="collections"
      :reload="true"
    />
  </v-container>
</template>

<script>
import SearchResultCard from '@/components/collection/SearchResultCard.vue';

export default {
  computed: {
    component() {
      return SearchResultCard;
    },
  },
  components: {
    DataIterator: () => import('@/components/utils/DataIterator.vue'),
    SearchBar: () => import('@/components/utils/ExtendedBar.vue'),
    // eslint-disable-next-line
    SearchResultCard,
  },
};
</script>

<style scoped>
.container,
.container > div {
  height: 100%;
}

.row > .col:empty {
  display: none;
}
</style>
