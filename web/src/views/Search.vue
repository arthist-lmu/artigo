<template>
  <v-container class="pa-0">
    <v-alert>
      <v-col class="d-flex pa-0 align-center">
        <div>{{ $tc('search.fields.results', total) }}</div>

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
              <span>{{ $t('search.fields.per-page') }}</span>
            </template>
          </v-select>
        </div>

        <v-spacer />

        <v-checkbox
          v-model="display.tags"
          class="mt-0 pt-0 ml-4"
          :label="$t('search.fields.display-tags')"
          on-icon="mdi-check-circle-outline"
          off-icon="mdi-checkbox-blank-circle-outline"
          color="primary"
          hide-details
        />

        <v-checkbox
          v-model="display.metadata"
          class="mt-0 pt-0 ml-4"
          :label="$t('search.fields.display-metadata')"
          on-icon="mdi-check-circle-outline"
          off-icon="mdi-checkbox-blank-circle-outline"
          color="primary"
          hide-details
        />

        <ReconcileButton
          :entries="pageEntries"
          class="ml-3"
        />
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
        :cols="cols"
        :class="disabledEntries[entry.id] ? 'disabled' : ''"
      >
        <SearchResultCard
          v-model="disabledEntries[entry.id]"
          :entry="entry"
          :displayTags="display.tags"
          :displayMetadata="display.metadata"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      display: {
        tags: true,
        metadata: true,
      },
      disabledEntries: {},
      perPage: 10,
      perPageItems: [
        10,
        25,
        50,
        100,
      ],
      page: 1,
    };
  },
  computed: {
    total() {
      return this.$store.state.search.data.total;
    },
    offset() {
      return this.$store.state.search.data.offset;
    },
    entries() {
      const { entries } = this.$store.state.search.data;
      return entries || [];
    },
    pageEntries() {
      const firstEntry = (this.page - 1) * this.perPage - this.offset;
      const lastEntry = firstEntry + this.perPage;
      return this.entries.slice(firstEntry, lastEntry);
    },
    nPages() {
      return Math.ceil(this.total / this.perPage);
    },
    cols() {
      if (!this.display.metadata) {
        if (!this.display.tags) {
          return 3;
        }
        return 6;
      }
      return 12;
    },
  },
  watch: {
    entries() {
      if (this.offset === 0) {
        this.page = 1;
      }
    },
    page(value) {
      const lastEntry = this.entries.length + this.offset;
      const withLastEntry = this.total === lastEntry;
      if (
        ((value * this.perPage > lastEntry) && !withLastEntry)
        || (value * this.perPage <= this.offset)
      ) {
        const offset = (value - 1) * this.perPage;
        this.$store.dispatch('search/post', { offset, sourceView: true });
      }
      window.scrollTo(0, 0);
    },
    display: {
      handler({ tags, metadata }) {
        this.$store.dispatch('settings/setDisplay', { type: 'tags', value: tags });
        this.$store.dispatch('settings/setDisplay', { type: 'metadata', value: metadata });
      },
      deep: true,
    },
  },
  created() {
    const { display } = this.$store.state.settings;
    this.display.tags = display.tags;
    this.display.metadata = display.metadata;
  },
  mounted() {
    // TODO: test properly
    this.$store.dispatch('search/getURLParams', this.$route.query);
    window.onpopstate = () => {
      this.$store.commit('search/toggleBackBtn');
      this.$store.dispatch('search/getURLParams', this.$route.query);
    };
  },
  components: {
    SearchResultCard: () => import('@/components/SearchResultCard.vue'),
    ReconcileButton: () => import('@/components/ReconcileButton.vue'),
  },
};
</script>
