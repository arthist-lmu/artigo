<template>
  <v-container class="pt-0">
    <SearchBar />

    <v-data-iterator
      :items="entries"
      :items-per-page.sync="itemsPerPage"
      :page.sync="page"
      class="d-flex flex-column"
      :class="isMobile ? 'mx-n2' : undefined"
      hide-default-footer
    >
      <template v-slot:default="props">
        <v-row class="ma-n1">
          <v-col
            v-for="entry in props.items"
            :key="entry.resource_id"
            :cols="(12 / itemsPerRow)"
            class="pa-1"
          >
            <ResultCard :entry="entry" />
          </v-col>
        </v-row>
      </template>

      <template v-slot:no-data>
        <v-row justify="center">
          <v-col
            :cols="noDataCols"
            align-self="center"
          >
            <v-alert
              class="mb-0"
              type="error"
              icon="mdi-alert-circle-outline"
              colored-border
            >
              {{ $t('search.fields.no-results') }}
            </v-alert>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      page: 1,
    };
  },
  computed: {
    entries() {
      return this.$store.state.search.data.entries;
    },
    itemsPerPage() {
      return this.$store.state.search.itemsPerPage;
    },
    itemsPerRow() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 1;
        case 'sm': return 2;
        case 'md': return 3;
        case 'lg': return 4;
        default: return 6;
      }
    },
    noDataCols() {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 12;
        case 'sm': return 9;
        case 'md': return 6;
        case 'lg': return 4;
        default: return 3;
      }
    },
    isMobile() {
      return this.$vuetify.breakpoint.mobile;
    },
  },
  mounted() {
    this.$store.dispatch('search/getURLParams', this.$route.query);
    window.onpopstate = () => {
      this.$store.commit('search/toggleBackBtn');
      this.$store.dispatch('search/getURLParams', this.$route.query);
    };
  },
  components: {
    SearchBar: () => import('@/components/ExtendedSearchBar.vue'),
    ResultCard: () => import('@/components/SearchResultCard.vue'),
  },
};
</script>

<style>
.v-data-iterator > div {
  height: 100%;
}
</style>

<style scoped>
.container,
.container > div,
.container .justify-center {
  height: 100%;
}
</style>
