<template>
  <v-container class="pa-0">
    <v-alert>
      <v-col class="d-flex pa-0 align-center">
        <div>{{ $tc('search.fields.results', entries.length) }}</div>

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
          hide-details
        />

        <v-checkbox
          v-model="display.metadata"
          class="mt-0 pt-0 ml-4"
          :label="$t('search.fields.display-metadata')"
          hide-details
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
      no-gutters
    >
      <SearchResultCard
        v-for="entry in pageEntries"
        :key="entry.id"
        :entry="entry"
        :displayTags="display.tags"
        :displayMetadata="display.metadata"
      />
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
    entries() {
      const { entries } = this.$store.state.api.data;
      return entries || [];
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
    entries() {
      // TODO: what to display if there are no results?
      this.page = 1;
    },
    page() {
      window.scrollTo(0, 0);
    },
  },
  components: {
    SearchResultCard: () => import('@/components/SearchResultCard.vue'),
  },
};
</script>

<style>
.v-pagination__item, .v-pagination__navigation {
  box-shadow: none;
}

.v-alert .v-select .v-input__control {
  max-width: 65px;
  min-height: 14px;
}

.v-alert .v-select .v-input__append-outer {
  display: flex;
  align-items: center;
  margin-top: 0;
  margin-bottom: 0;
  height: 24px;
}

.v-alert .v-select .v-select__selection {
  margin-top: 0;
}
</style>
