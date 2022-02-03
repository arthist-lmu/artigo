<template>
  <v-container class="pa-0">
    <v-alert>
      <v-col class="d-flex pa-0 align-center">
        <div>{{ $tc('collection.fields.results', entries.length) }}</div>

        <div style="width: 290px;">
          <v-select
            v-model="perPage"
            :items="perPageItems"
            class="ml-4"
            hide-details
            dense
            flat
          >
            <template slot="append-outer">
              <span>{{ $t('collection.fields.per-page') }}</span>
            </template>
          </v-select>
        </div>
      </v-col>
    </v-alert>

    <v-pagination
      v-if="nPages > 1"
      v-model="page"
      :length="nPages"
      :total-visible="6"
      class="my-4"
      color="accent"
      circle
    />

    <v-row
      v-if="entries.length > 0"
      class="v-card v-card--flat v-sheet theme--light"
      no-gutters
    >
      <v-col
        v-for="entry in pageEntries"
        :key="entry.id"
        :class="disabledEntries[entry.id] ? 'disabled' : ''"
        cols="3"
      >
        <CollectionResultCard
          v-model="disabledEntries[entry.id]"
          :entry="entry"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      disabledEntries: {},
      perPage: 12,
      perPageItems: [
        12,
        24,
        48,
        96,
      ],
      page: 1,
    };
  },
  methods: {
    getData(name) {
      const query = { source: `+${name}` };
      const params = { query, limit: 250, sourceView: true };
      this.$store.dispatch('search/post', params);
    },
  },
  computed: {
    entries() {
      const { entries } = this.$store.state.search.data;
      return entries || [];
    },
    title() {
      return this.capitalize(this.entries[0].source.name);
    },
    pageEntries() {
      const firstEntry = (this.page - 1) * this.perPage;
      const lastEntry = firstEntry + this.perPage;
      return this.entries.slice(firstEntry, lastEntry);
    },
    nPages() {
      return Math.ceil(this.entries.length / this.perPage);
    },
  },
  watch: {
    '$route.params.name': function (name) {
      this.getData(name);
    },
    entries() {
      document.title = `${this.title} | ARTigo – Social Image Tagging`;
      this.page = 1;
    },
    page() {
      window.scrollTo(0, 0);
    },
  },
  created() {
    this.getData(this.$route.params.name);
  },
  components: {
    CollectionResultCard: () => import('@/components/CollectionResultCard.vue'),
  },
};
</script>
