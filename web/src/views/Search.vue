<template>
  <v-container class="pt-0">
    <SearchBar
      store="search"
      :height="height"
      :filter="true"
    >
      <template v-slot:append-item>
        <v-row
          v-for="aggregation in aggregations"
          :key="aggregation.field"
          class="aggregate"
        >
          <v-col v-if="aggregation.entries.length">
            <v-slide-group show-arrows>
              <v-slide-item
                v-for="entry in aggregation.entries"
                :key="entry.name"
              >
                <v-chip
                  @click="search(entry.name)"
                  class="mx-1"
                  depressed
                  outlined
                  rounded
                >
                  {{ entry.name }}
                </v-chip>
              </v-slide-item>
            </v-slide-group>
          </v-col>
        </v-row>
      </template>
    </SearchBar>

    <v-data-iterator
      :items="entries"
      :items-per-page.sync="itemsPerPage"
      :page.sync="page"
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
            <SearchResultCard :entry="entry" />
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
  methods: {
    search(value) {
      const query = { tags: value };
      this.$store.dispatch('search/post', { query });
    },
  },
  computed: {
    entries() {
      return this.$store.state.search.data.entries;
    },
    aggregations() {
      return this.$store.state.search.data.aggregations;
    },
    height() {
      let height = 100;
      if (this.aggregations.length) {
        this.aggregations.forEach((aggregation) => {
          if (aggregation.entries.length) {
            height += 56;
          }
        });
      }
      return height;
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
  },
  mounted() {
    this.$store.dispatch('search/getURLParams', this.$route.query);
    window.onpopstate = () => {
      this.$store.commit('search/toggleBackBtn');
      this.$store.dispatch('search/getURLParams', this.$route.query);
    };
  },
  components: {
    SearchBar: () => import('@/components/utils/ExtendedBar.vue'),
    SearchResultCard: () => import('@/components/search/SearchResultCard.vue'),
  },
};
</script>

<style>
.v-data-iterator > div:not(.row) {
  height: 100%;
}
</style>

<style scoped>
.container,
.container > div,
.container .justify-center {
  height: 100%;
}

.row > .col:empty {
  display: none;
}
</style>
